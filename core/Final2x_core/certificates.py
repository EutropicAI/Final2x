import os
import re
import ssl
import sys
from pathlib import Path


def configure_ssl_certificates() -> None:
    """Initialize native system trust for the macOS CLI before network imports."""
    if sys.platform != "darwin":
        return

    import truststore

    ca_file = os.environ.get("SSL_CERT_FILE")
    ca_directory = os.environ.get("SSL_CERT_DIR")
    directory_certificates: list[Path] = []
    if ca_directory:
        # OpenSSL capath uses hash.N filenames (including rehash symlinks).
        # It loads these lazily, but Security.framework only receives already
        # loaded certificates. Resolve and load them explicitly instead.
        for directory in ca_directory.split(os.pathsep):
            if not directory:
                continue
            for certificate in sorted(Path(directory).iterdir()):
                if re.fullmatch(r"[0-9a-fA-F]{8}\.\d+", certificate.name) and certificate.is_file():
                    directory_certificates.append(certificate)

    # Invalid explicit CA settings are installation/configuration errors.
    # Check them before injecting or importing cccv/torch, rather than hiding
    # the error behind a later model-download failure.
    if ca_file or directory_certificates:
        context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        if ca_file:
            context.load_verify_locations(cafile=ca_file)
        for certificate in directory_certificates:
            context.load_verify_locations(cafile=certificate)

    if directory_certificates:
        original_load_default_certs = truststore.SSLContext.load_default_certs

        def load_default_certs(context: truststore.SSLContext, purpose: ssl.Purpose = ssl.Purpose.SERVER_AUTH) -> None:
            original_load_default_certs(context, purpose)
            for certificate in directory_certificates:
                context.load_verify_locations(cafile=certificate)

        # Keep SSL_CERT_DIR's default-context semantics while eagerly loading
        # its additional anchors for truststore's macOS verifier.
        truststore.SSLContext.load_default_certs = load_default_certs  # type: ignore[method-assign]

    truststore.inject_into_ssl()
