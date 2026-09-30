import subprocess
import sys


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
