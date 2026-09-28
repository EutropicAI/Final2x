import os
import sys

import certifi


def configure_ssl_certificates() -> None:
    if sys.platform == "darwin":
        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
