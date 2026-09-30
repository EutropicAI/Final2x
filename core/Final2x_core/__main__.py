import argparse
import os
import sys
from pathlib import Path

from Final2x_core.certificates import configure_ssl_certificates

configure_ssl_certificates()

from loguru import logger

from Final2x_core.config import SRConfig
from Final2x_core.SRqueue import sr_queue

if getattr(sys, "frozen", False):
    # frozen
    _IS_FROZEN_ = True
    projectPATH = Path(sys.executable).parent.absolute()
else:
    # unfrozen
    _IS_FROZEN_ = False
    projectPATH = Path(__file__).resolve().parent.absolute()

# parse args
parser = argparse.ArgumentParser()
parser.description = "when para is not specified, the config.yaml file in the directory will be read automatically"
parser.add_argument("-b", "--BASE64", help="base64 string for config json", type=str)
parser.add_argument("-j", "--JSON", help="JSON string for config", type=str)
parser.add_argument("-y", "--YAML", help="yaml config file path", type=str)
parser.add_argument("-l", "--LOG", help="save log", action="store_true")
parser.add_argument("-n", "--NOTOPENFOLDER", help="don't open output folder", action="store_true")
args = parser.parse_args()


def open_folder(path: str) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            os.system('open "{}"'.format(path))
        elif sys.platform.startswith("linux"):
            os.system('xdg-open "{}"'.format(path))
        else:
            logger.error("cannot open output folder")
    except Exception as e:
        logger.error(e)
        logger.error("cannot open output folder")


def main() -> None:
    if args.LOG:
        # init logger
        logger.add(projectPATH / "logs" / "log-{time}.log", encoding="utf-8", retention="60 days")

    # load config
    config: SRConfig
    if args.BASE64 is not None:
        config = SRConfig.from_base64(str(args.BASE64))
    elif args.JSON is not None:
        config = SRConfig.from_json_str(str(args.JSON))
    elif args.YAML is not None:
        config = SRConfig.from_yaml(str(args.YAML))
    else:
        config = SRConfig.from_yaml(projectPATH / "config.yaml")

    logger.info("config loaded")
    logger.debug("output path: " + str(config.output_path))

    sr_queue(config=config)

    logger.success("______SR_COMPLETED______")

    if not args.NOTOPENFOLDER:
        OP = Path(config.output_path) / "outputs"
        open_folder(str(OP))


if __name__ == "__main__":
    main()
