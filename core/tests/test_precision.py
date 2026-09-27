from types import SimpleNamespace
from unittest.mock import patch

import pytest

from Final2x_core import SRConfig, SRWrapper

from .util import CONFIG_PATH


@pytest.mark.parametrize(("precision", "use_fp16"), [("fp32", False), ("fp16", True)])
def test_precision_is_passed_to_cccv(precision: str, use_fp16: bool) -> None:
    config_data = SRConfig.from_yaml(CONFIG_PATH).model_dump()
    config_data["precision"] = precision
    config = SRConfig(**config_data)

    with patch("Final2x_core.SRclass.AutoModel.from_pretrained", return_value=SimpleNamespace(device="cpu")) as model:
        SRWrapper(config)

    assert model.call_args.kwargs["fp16"] is use_fp16


def test_precision_defaults_to_fp32_and_rejects_unsupported_values() -> None:
    config_data = SRConfig.from_yaml(CONFIG_PATH).model_dump()
    config_data.pop("precision")
    assert SRConfig(**config_data).precision == "fp32"

    config_data["precision"] = "bf16"
    with pytest.raises(ValueError):
        SRConfig(**config_data)
