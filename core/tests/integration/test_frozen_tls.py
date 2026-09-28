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
    binary: Path, directory: Path, url: str, *, ca_file: Path | None = None
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
    # Restrict only this child process, not the machine's trust configuration.
    # A missing/unreadable system CA must not break the bundled certifi CA.
    paths = ssl.get_default_verify_paths()
    denied = [
        '(subpath "/private/etc/ssl")',
        '(subpath "/etc/ssl")',
        '(subpath "/opt/homebrew/etc/openssl@3")',
        '(subpath "/usr/local/etc/openssl@3")',
        f"(literal {json.dumps(paths.openssl_cafile)})",
        f"(subpath {json.dumps(paths.openssl_capath)})",
    ]
    profile = f"(version 1) (allow default) (deny file-read* {' '.join(denied)})"
    assert shutil.which("sandbox-exec"), "macOS sandbox-exec is required for the missing-system-CA test"
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
def self_signed_server(downloaded_model: Path, tmp_path_factory: pytest.TempPathFactory) -> Iterator[tuple[str, Path]]:
    directory = tmp_path_factory.mktemp("frozen-tls-server")
    certificate = directory / "certificate.pem"
    key = directory / "key.pem"
    config = directory / "openssl.cnf"
    config.write_text(
        "[req]\nprompt=no\ndistinguished_name=dn\nx509_extensions=extensions\n"
        "[dn]\nCN=localhost\n[extensions]\nsubjectAltName=IP:127.0.0.1,DNS:localhost\n"
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
            str(key),
            "-out",
            str(certificate),
            "-config",
            str(config),
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
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
        yield f"https://127.0.0.1:{server.server_port}/", certificate
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_frozen_download_without_system_ca(downloaded_model: Path) -> None:
    assert downloaded_model.stat().st_size > 0


def test_frozen_rejects_self_signed_certificate(
    frozen_core: Path,
    self_signed_server: tuple[str, Path],
    tmp_path: Path,
) -> None:
    url, _ = self_signed_server
    result = run_core(frozen_core, tmp_path / "untrusted", url)
    assert result.returncode != 0
    assert "CERTIFICATE_VERIFY_FAILED" in result.stdout + result.stderr
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
