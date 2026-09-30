from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from Final2x_core.config import SRConfig
    from Final2x_core.SRclass import SRWrapper
    from Final2x_core.SRqueue import sr_queue

__all__ = ["SRConfig", "SRWrapper", "sr_queue"]
_EXPORT_MODULES = {"SRConfig": "config", "SRWrapper": "SRclass", "sr_queue": "SRqueue"}


def __getattr__(name: str) -> Any:
    # Keep the public API without loading cccv/torch before CLI SSL setup.
    if name not in _EXPORT_MODULES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(f".{_EXPORT_MODULES[name]}", __name__), name)
    globals()[name] = value
    return value
