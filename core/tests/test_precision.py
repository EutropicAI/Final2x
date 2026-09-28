import inspect
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from cccv import AutoModel

from Final2x_core import SRConfig, SRWrapper

from .util import CONFIG_PATH


@pytest.mark.parametrize(
    ("precision", "use_fp16", "use_bf16"),
    [("fp32", False, False), ("fp16", True, False), ("bf16", False, True)],
)
def test_precision_is_passed_to_cccv(precision: str, use_fp16: bool, use_bf16: bool) -> None:
    config_data = SRConfig.from_yaml(CONFIG_PATH).model_dump()
    config_data["precision"] = precision
    config = SRConfig(**config_data)

    with patch("Final2x_core.SRclass.AutoModel.from_pretrained", return_value=SimpleNamespace(device="cpu")) as model:
        SRWrapper(config)

    assert model.call_args.kwargs["fp16"] is use_fp16
    assert model.call_args.kwargs["bf16"] is use_bf16


def test_cccv_exposes_bf16_argument() -> None:
    # Older releases silently accepted bf16 via **kwargs but ran in FP32.
    assert "bf16" in inspect.signature(AutoModel.from_pretrained).parameters


def test_precision_defaults_to_fp32_and_rejects_unsupported_values() -> None:
    config_data = SRConfig.from_yaml(CONFIG_PATH).model_dump()
    config_data.pop("precision")
    assert SRConfig(**config_data).precision == "fp32"

    config_data["precision"] = "invalid"
    with pytest.raises(ValueError):
        SRConfig(**config_data)
