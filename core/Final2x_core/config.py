import base64
import json
from pathlib import Path
from typing import Any, List, Literal, Optional, Union

import yaml
from cccv import ConfigType
from pydantic import BaseModel, DirectoryPath, FilePath, field_validator


class SRConfig(BaseModel):
    pretrained_model_name: Union[ConfigType, str]
    device: str
    use_tile: Optional[bool] = None
    precision: Literal["fp32", "fp16"] = "fp32"
    gh_proxy: Optional[str] = None
    target_scale: Optional[Union[int, float]] = None
    output_path: DirectoryPath
    input_path: List[FilePath]
    save_format: Optional[str] = ".png"

    @classmethod
    def from_yaml(cls, yaml_path: Union[Path, str]) -> Any:
        with open(yaml_path, "r", encoding="utf-8") as f:
            try:
                config = yaml.safe_load(f)
            except Exception as e:
                raise ValueError(f"Error loading config: {e}")

        cfg = cls(**config)
        if cfg.target_scale is None or cfg.target_scale <= 0:
            cfg.target_scale = 2
        return cfg

    @classmethod
    def from_json_str(cls, json_str: str) -> Any:
        try:
            config = json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Error loading config: {e}")

        cfg = cls(**config)
        if cfg.target_scale is None or cfg.target_scale <= 0:
            cfg.target_scale = 2
        return cfg

    @classmethod
    def from_base64(cls, base64_str: str) -> Any:
        try:
            config_bytes = base64_str.encode("utf-8")
            config_json_str = base64.b64decode(config_bytes).decode("utf-8")
        except Exception as e:
            raise ValueError(f"Error loading config: {e}")

        return cls.from_json_str(config_json_str)

    @field_validator("device")
    def device_match(cls, v: str) -> str:
        device_list = ["auto", "cpu", "cuda", "mps", "directml", "xpu"]
        for d in device_list:
            if v.startswith(d):
                return v

        raise ValueError(f"device must start with {device_list}")
