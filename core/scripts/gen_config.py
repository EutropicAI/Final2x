import os
from pathlib import Path

import yaml
from cccv import ConfigType

projectPATH = Path(__file__).resolve().parent.parent.absolute()

if os.environ.get("GITHUB_ACTIONS") == "true":
    _DEVICE_ = "cpu"
else:
    _DEVICE_ = "auto"

print("-" * 50)


def gen_config() -> None:
    if _DEVICE_ == "cpu":
        print("GitHub Actions detected. Using CPU.")

    p_dict = {
        "pretrained_model_name": ConfigType.RealESRGAN_AnimeJaNai_HD_V3_Compact_2x.value,
        "device": _DEVICE_,
        "use_tile": True,
        "precision": "fp32",
        "gh_proxy": None,
        "target_scale": None,
        "output_path": str(projectPATH / "assets"),
        "input_path": [
            str(projectPATH / "assets" / "gray.jpg"),
            str(projectPATH / "assets" / "herta.jpg"),
            str(projectPATH / "assets" / "final2x-10.png"),
            str(projectPATH / "assets" / "final2x-10.png"),
            str(projectPATH / "assets" / "final2x-20.png"),
            str(projectPATH / "assets" / "final2x-40.png"),
            str(projectPATH / "assets" / "final2x-80.png"),
            str(projectPATH / "assets" / "final2x-160.png"),
            str(projectPATH / "assets" / "final2x-320.png"),
            str(projectPATH / "assets" / "herta-unix-pic.exe"),
            str(projectPATH / "assets" / "vulkan-1.dll"),
        ],
        "save_format": ".png",
    }

    p_yaml = str(projectPATH / "Final2x_core/config.yaml")

    with open(p_yaml, "w", encoding="utf-8") as f:
        yaml.safe_dump(p_dict, f)

    print("Config generated at " + p_yaml)


if __name__ == "__main__":
    gen_config()
