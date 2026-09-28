from types import SimpleNamespace

import certifi
from pytest import MonkeyPatch

from Final2x_core.util import certificates


def test_macos_uses_bundled_ca_when_not_configured(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(certificates, "sys", SimpleNamespace(platform="darwin"))
    monkeypatch.delenv("SSL_CERT_FILE", raising=False)

    certificates.configure_ssl_certificates()

    assert certificates.os.environ["SSL_CERT_FILE"] == certifi.where()


def test_macos_preserves_explicit_ca_path(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(certificates, "sys", SimpleNamespace(platform="darwin"))
    monkeypatch.setenv("SSL_CERT_FILE", "/custom/ca.pem")

    certificates.configure_ssl_certificates()

    assert certificates.os.environ["SSL_CERT_FILE"] == "/custom/ca.pem"
