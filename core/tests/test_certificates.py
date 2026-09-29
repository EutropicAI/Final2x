import os
import ssl
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from Final2x_core.util import certificates


@pytest.fixture
def native_context(monkeypatch: MonkeyPatch) -> Mock:
    context = Mock()
    factory = Mock(return_value=context)
    monkeypatch.setitem(sys.modules, "truststore", SimpleNamespace(SSLContext=factory))
    monkeypatch.setattr(certificates, "sys", SimpleNamespace(platform="darwin"))
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)
    monkeypatch.delenv("SSL_CERT_DIR", raising=False)
    return context


def test_macos_uses_native_context_without_mutating_ssl_or_environment(
    monkeypatch: MonkeyPatch, native_context: Mock
) -> None:
    handler = Mock()
    opener = Mock()
    handler_factory = Mock(return_value=handler)
    opener_factory = Mock(return_value=opener)
    install = Mock()
    monkeypatch.setattr(certificates, "HTTPSHandler", handler_factory)
    monkeypatch.setattr(certificates, "build_opener", opener_factory)
    monkeypatch.setattr(certificates, "install_opener", install)
    original_context = ssl.SSLContext
    original_environment = os.environ.copy()

    certificates.configure_ssl_certificates()

    factory = sys.modules["truststore"].SSLContext  # type: ignore[attr-defined]
    factory.assert_called_once_with(ssl.PROTOCOL_TLS_CLIENT)
    handler_factory.assert_called_once_with(context=native_context)
    opener_factory.assert_called_once_with(handler)
    install.assert_called_once_with(opener)
    native_context.load_verify_locations.assert_not_called()
    assert ssl.SSLContext is original_context
    assert os.environ == original_environment


@pytest.mark.parametrize(
    ("ca_file", "ca_directory"),
    [("/custom/ca.pem", None), (None, "/custom/certs"), ("/custom/ca.pem", "/custom/certs")],
)
def test_macos_preserves_explicit_ca_settings(
    monkeypatch: MonkeyPatch, native_context: Mock, ca_file: str | None, ca_directory: str | None
) -> None:
    if ca_file:
        monkeypatch.setenv("SSL_CERT_FILE", ca_file)
    if ca_directory:
        monkeypatch.setenv("SSL_CERT_DIR", ca_directory)
    monkeypatch.setattr(certificates, "HTTPSHandler", Mock())
    monkeypatch.setattr(certificates, "build_opener", Mock())
    monkeypatch.setattr(certificates, "install_opener", Mock())
    original_environment = os.environ.copy()

    certificates.configure_ssl_certificates()

    native_context.load_verify_locations.assert_called_once_with(cafile=ca_file, capath=ca_directory)
    assert os.environ == original_environment


def test_invalid_explicit_ca_is_not_silently_ignored(monkeypatch: MonkeyPatch, native_context: Mock) -> None:
    monkeypatch.setenv("SSL_CERT_FILE", "/missing/ca.pem")
    native_context.load_verify_locations.side_effect = FileNotFoundError("CA file is missing")
    install = Mock()
    monkeypatch.setattr(certificates, "install_opener", install)

    with pytest.raises(FileNotFoundError, match="CA file is missing"):
        certificates.configure_ssl_certificates()

    install.assert_not_called()


@pytest.mark.parametrize("platform", ["win32", "linux"])
def test_other_platforms_are_unchanged(monkeypatch: MonkeyPatch, platform: str) -> None:
    monkeypatch.setattr(certificates, "sys", SimpleNamespace(platform=platform))
    monkeypatch.setitem(sys.modules, "truststore", None)
    monkeypatch.setenv("SSL_CERT_FILE", "/existing/ca.pem")
    install = Mock()
    monkeypatch.setattr(certificates, "install_opener", install)
    original_context = ssl.SSLContext
    original_environment = os.environ.copy()

    certificates.configure_ssl_certificates()

    install.assert_not_called()
    assert ssl.SSLContext is original_context
    assert os.environ == original_environment
