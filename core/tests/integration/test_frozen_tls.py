"""Exercise real model downloads through the macOS PyInstaller executable.

Set FINAL2X_TEST_BINARY to the frozen executable to enable these tests.
No Python packages from the source environment are used by the executable.
"""

from __future__ import annotations

import json
import os
import shutil
import ssl
import subprocess
import sys
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

MODEL_NAME = "RealESRGAN_AnimeJaNai_HD_V3_Compact_2x.pth"
MODEL_ZOO = "https://github.com/EutropicAI/cccv/releases/download/model_zoo/"
IMAGE_PATH = Path(__file__).resolve().parents[2] / "assets/gray.jpg"
pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="macOS frozen TLS regression tests")


@pytest.fixture(scope="module")
def frozen_core() -> Path:
    value = os.environ.get("FINAL2X_TEST_BINARY")
    if not value:
        pytest.skip("Set FINAL2X_TEST_BINARY to test the PyInstaller executable")
    binary = Path(value).resolve()
    assert binary.is_file(), f"Frozen executable not found: {binary}"
    return binary


def run_core(
    binary: Path, directory: Path, url: str, *, ca_file: Path | None = None, ca_directory: Path | None = None
) -> subprocess.CompletedProcess[str]:
    directory.mkdir(parents=True)
    cache = directory / "cache"
    output = directory / "output"
    cache.mkdir()
    output.mkdir()
    env = os.environ.copy()
    for name in (
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "REQUESTS_CA_BUNDLE",
        "CURL_CA_BUNDLE",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        env.pop(name, None)
    env["CCCV_CACHE_MODEL_DIR"] = str(cache)
    env["CCCV_REMOTE_MODEL_ZOO"] = url
    if ca_file is not None:
        env["SSL_CERT_FILE"] = str(ca_file)
    if ca_directory is not None:
        env["SSL_CERT_DIR"] = str(ca_directory)
    config = {
        "pretrained_model_name": MODEL_NAME,
        "device": "cpu",
        "gh_proxy": None,
        "target_scale": None,
        "output_path": str(output),
        "input_path": [str(IMAGE_PATH)],
        "use_tile": False,
        "save_format": ".png",
    }
    # Isolate development-environment CA files without changing system trust.
    # Native Security.framework validation must not depend on Homebrew or a
    # bundled PEM file. Keep the OS trust service and keychains accessible.
    denied = [
        '(subpath "/opt/homebrew/etc/openssl@3")',
        '(subpath "/usr/local/etc/openssl@3")',
        '(subpath "/private/etc/ssl")',
        '(subpath "/etc/ssl")',
    ]
    profile = f"(version 1) (allow default) (deny file-read* {' '.join(denied)})"
    assert shutil.which("sandbox-exec"), "macOS sandbox-exec is required to isolate filesystem CA bundles"
    result = subprocess.run(
        ["sandbox-exec", "-p", profile, str(binary), "-j", json.dumps(config), "-n"],
        env=env,
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )
    (directory / "core.log").write_text(result.stdout + result.stderr)
    return result


@pytest.fixture(scope="module")
def downloaded_model(frozen_core: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("frozen-tls-public")
    result = run_core(frozen_core, directory / "download", MODEL_ZOO)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "______SR_COMPLETED______" in result.stderr
    model = directory / "download/cache" / MODEL_NAME
    assert model.is_file()
    assert (directory / "download/output/outputs/2x-gray.png").is_file()
    return model


@pytest.fixture(scope="module")
def self_signed_server(
    downloaded_model: Path, tmp_path_factory: pytest.TempPathFactory, request: pytest.FixtureRequest
) -> Iterator[tuple[str, Path]]:
    directory = tmp_path_factory.mktemp("frozen-tls-server")
    kind = getattr(request, "param", "valid")
    ca_certificate = directory / "ca.pem"
    ca_key = directory / "ca.key"
    certificate = directory / "certificate.pem"
    key = directory / "key.pem"
    csr = directory / "server.csr"
    config = directory / "openssl.cnf"
    config.write_text(
        "[req]\nprompt=no\ndistinguished_name=dn\nx509_extensions=extensions\n"
        "[dn]\nCN=Final2x temporary test CA\n[extensions]\n"
        "basicConstraints=critical,CA:TRUE\nkeyUsage=critical,digitalSignature,keyEncipherment,keyCertSign\n"
    )
    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-days",
            "1",
            "-keyout",
            str(ca_key),
            "-out",
            str(ca_certificate),
            "-config",
            str(config),
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    subprocess.run(
        [
            "openssl",
            "req",
            "-new",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-keyout",
            str(key),
            "-out",
            str(csr),
            "-subj",
            "/CN=localhost",
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    extensions = directory / "server.cnf"
    subject_alt_name = "DNS:wrong-host.invalid" if kind == "wrong-host" else "IP:127.0.0.1,DNS:localhost"
    extensions.write_text(
        "basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\n"
        f"extendedKeyUsage=serverAuth\nsubjectAltName={subject_alt_name}\n"
    )
    if kind == "expired":
        (directory / "index.txt").touch()
        (directory / "serial").write_text("01\n")
        ca_config = directory / "ca.cnf"
        ca_config.write_text(
            "[ca]\ndefault_ca=issuer\n[issuer]\n"
            f"database={directory / 'index.txt'}\nnew_certs_dir={directory}\nserial={directory / 'serial'}\n"
            f"certificate={ca_certificate}\nprivate_key={ca_key}\n"
            "default_md=sha256\npolicy=subject\n[subject]\ncommonName=supplied\n"
        )
        sign_command = [
            "openssl",
            "ca",
            "-batch",
            "-notext",
            "-config",
            str(ca_config),
            "-in",
            str(csr),
            "-out",
            str(certificate),
            "-extfile",
            str(extensions),
            "-startdate",
            "200101000000Z",
            "-enddate",
            "200102000000Z",
        ]
    else:
        sign_command = [
            "openssl",
            "x509",
            "-req",
            "-in",
            str(csr),
            "-CA",
            str(ca_certificate),
            "-CAkey",
            str(ca_key),
            "-CAcreateserial",
            "-out",
            str(certificate),
            "-days",
            "1",
            "-extfile",
            str(extensions),
        ]
    subprocess.run(sign_command, check=True, capture_output=True, timeout=30)
    model_bytes = downloaded_model.read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.send_header("Content-Length", str(len(model_bytes)))
            self.end_headers()
            self.wfile.write(model_bytes)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certificate, key)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"https://127.0.0.1:{server.server_port}/", ca_certificate
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_frozen_download_uses_system_trust_without_ca_files(downloaded_model: Path) -> None:
    assert downloaded_model.stat().st_size > 0


def test_frozen_does_not_bundle_ca_certificates(frozen_core: Path) -> None:
    assert not list(frozen_core.parent.rglob("cacert.pem")), "A static CA bundle was included in the frozen app"
    assert not list(frozen_core.parent.rglob("certifi")), "certifi was included in the frozen app"


def test_frozen_rejects_self_signed_certificate(
    frozen_core: Path,
    self_signed_server: tuple[str, Path],
    tmp_path: Path,
) -> None:
    url, _ = self_signed_server
    result = run_core(frozen_core, tmp_path / "untrusted", url)
    assert result.returncode != 0
    # Security.framework errors are localized and do not use OpenSSL's wording.
    assert "ssl.SSLCertVerificationError" in result.stdout + result.stderr
    assert not (tmp_path / "untrusted/cache" / MODEL_NAME).exists()


def test_frozen_preserves_explicit_custom_ca(
    frozen_core: Path,
    self_signed_server: tuple[str, Path],
    tmp_path: Path,
) -> None:
    url, certificate = self_signed_server
    result = run_core(frozen_core, tmp_path / "trusted", url, ca_file=certificate)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "______SR_COMPLETED______" in result.stderr
    assert (tmp_path / "trusted/output/outputs/2x-gray.png").is_file()


def test_frozen_preserves_explicit_ca_directory(
    frozen_core: Path,
    self_signed_server: tuple[str, Path],
    tmp_path: Path,
) -> None:
    url, certificate = self_signed_server
    directory = tmp_path / "certs"
    directory.mkdir()
    shutil.copyfile(certificate, directory / "private-ca.pem")
    # macOS LibreSSL lacks `rehash` and even returns 0 for that unknown command.
    # x509 -subject_hash works with both LibreSSL and OpenSSL.
    ca_hash = subprocess.run(
        ["openssl", "x509", "-in", str(certificate), "-noout", "-subject_hash"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    ).stdout.strip()
    assert len(ca_hash) == 8
    (directory / f"{ca_hash}.0").symlink_to("private-ca.pem")
    result = run_core(frozen_core, tmp_path / "trusted-directory", url, ca_directory=directory)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "______SR_COMPLETED______" in result.stderr
    assert (tmp_path / "trusted-directory/output/outputs/2x-gray.png").is_file()


@pytest.mark.parametrize("self_signed_server", ["expired", "wrong-host"], indirect=True)
def test_frozen_rejects_invalid_certificate_even_with_trusted_ca(
    frozen_core: Path, self_signed_server: tuple[str, Path], tmp_path: Path
) -> None:
    url, certificate = self_signed_server
    result = run_core(frozen_core, tmp_path / "invalid", url, ca_file=certificate)
    assert result.returncode != 0
    assert "ssl.SSLCertVerificationError" in result.stdout + result.stderr
    assert not (tmp_path / "invalid/cache" / MODEL_NAME).exists()
