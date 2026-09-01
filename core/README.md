# Final2x-core

Final2x-core is the cross-platform image super-resolution CLI and desktop backend for Final2x.

### Install

Install the CLI from PyPI. Desktop builds bundle the matching core where required.

Make sure you have Python >= 3.9 and PyTorch >= 2.0 installed

```shell
pip install Final2x-core
```

### cli

```shell
usage: Final2x-core [-h] [-b BASE64] [-j JSON] [-y YAML] [-l] [-n]

when para is not specified, the config.yaml file in the directory will be read automatically

options:
  -h, --help            show this help message and exit
  -b BASE64, --BASE64 BASE64
                        base64 string for config json
  -j JSON, --JSON JSON  JSON string for config
  -y YAML, --YAML YAML  yaml config file path
  -l, --LOG             save log
  -n, --NOTOPENFOLDER   don't open output folder
```
