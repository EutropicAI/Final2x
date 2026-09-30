import os
import ssl
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from Final2x_core import certificates


@pytest.fixture
def native_context(monkeypatch: MonkeyPatch) -> Mock:
    context = Mock()
    factory = Mock(return_value=context)
    inject = Mock()
    monkeypatch.setitem(sys.modules, "truststore", SimpleNamespace(SSLContext=factory, inject_into_ssl=inject))
    monkeypatch.setattr(certificates, "sys", SimpleNamespace(platform="darwin"))
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.delenv("SSL_CERT_DIR", raising=False)
    return context


def test_macos_injects_system_trust_without_mutating_environment(native_context: Mock) -> None:
    original_environment = os.environ.copy()

    certificates.configure_ssl_certificates()

    sys.modules["truststore"].inject_into_ssl.assert_called_once()  # type: ignore[attr-defined]
    native_context.load_verify_locations.assert_not_called()
    assert os.environ == original_environment


def test_invalid_explicit_ca_file_is_not_silently_ignored(monkeypatch: MonkeyPatch, native_context: Mock) -> None:
    monkeypatch.setenv("SSL_CERT_FILE", "/missing/ca.pem")
    native_context.load_verify_locations.side_effect = FileNotFoundError("CA file is missing")

    with pytest.raises(FileNotFoundError, match="CA file is missing"):
        certificates.configure_ssl_certificates()

    sys.modules["truststore"].inject_into_ssl.assert_not_called()  # type: ignore[attr-defined]


def test_invalid_explicit_ca_directory_is_not_silently_ignored(
    monkeypatch: MonkeyPatch, native_context: Mock, tmp_path: Path
) -> None:
    monkeypatch.setenv("SSL_CERT_DIR", str(tmp_path / "missing"))

    with pytest.raises(FileNotFoundError):
        certificates.configure_ssl_certificates()

    sys.modules["truststore"].inject_into_ssl.assert_not_called()  # type: ignore[attr-defined]


@pytest.mark.parametrize("platform", ["win32", "linux"])
def test_other_platforms_are_unchanged(monkeypatch: MonkeyPatch, platform: str) -> None:
    monkeypatch.setattr(certificates, "sys", SimpleNamespace(platform=platform))
    monkeypatch.setitem(sys.modules, "truststore", None)
    monkeypatch.setenv("SSL_CERT_FILE", "/existing/ca.pem")
    monkeypatch.setenv("SSL_CERT_DIR", "/existing/certs")
    original_context = ssl.SSLContext
    original_environment = os.environ.copy()

    certificates.configure_ssl_certificates()

    assert ssl.SSLContext is original_context
    assert os.environ == original_environment


def test_library_import_keeps_public_exports_without_injecting_ssl() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import ssl, sys\n"
            "original = ssl.SSLContext\n"
            "import Final2x_core\n"
            "assert 'torch' not in sys.modules and 'cccv' not in sys.modules\n"
            "from Final2x_core import SRConfig, SRWrapper, sr_queue\n"
            "from Final2x_core.config import SRConfig as config\n"
            "from Final2x_core.SRclass import SRWrapper as wrapper\n"
            "from Final2x_core.SRqueue import sr_queue as queue\n"
            "assert (SRConfig, SRWrapper, sr_queue) == (config, wrapper, queue)\n"
            "assert ssl.SSLContext is original\n",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_injects_before_loading_cccv_and_torch() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy, ssl, sys\n"
            "original = ssl.SSLContext\n"
            "if sys.platform == 'darwin':\n"
            "    import truststore\n"
            "    inject = truststore.inject_into_ssl\n"
            "    def check_order():\n"
            "        assert 'torch' not in sys.modules and 'cccv' not in sys.modules\n"
            "        inject()\n"
            "    truststore.inject_into_ssl = check_order\n"
            "sys.argv = ['Final2x-core', '-h']\n"
            "try:\n"
            "    runpy.run_module('Final2x_core', run_name='__main__')\n"
            "except SystemExit as error:\n"
            "    assert error.code == 0\n"
            "assert (ssl.SSLContext is not original) == (sys.platform == 'darwin')\n",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
