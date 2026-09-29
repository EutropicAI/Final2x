import os
import ssl
import sys
from urllib.request import HTTPSHandler, build_opener, install_opener


def configure_ssl_certificates() -> None:
    """Use macOS system trust for this application's urllib downloads.

    PyTorch's model downloader uses urllib, so an explicit HTTPS context avoids
    changing ssl.SSLContext globally or depending on OpenSSL's build-time CA path.
    Windows and Linux retain their existing certificate and proxy handling.
    """
    if sys.platform != "darwin":
        return

    import truststore

    context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ca_file = os.environ.get("SSL_CERT_FILE")
    ca_directory = os.environ.get("SSL_CERT_DIR")
    if ca_file or ca_directory:
        # Explicit user certificates supplement native system trust. Invalid
        # paths must raise, rather than silently falling back to another CA set.
        context.load_verify_locations(cafile=ca_file, capath=ca_directory)
    install_opener(build_opener(HTTPSHandler(context=context)))
