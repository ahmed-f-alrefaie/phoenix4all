import pathlib
from typing import Type

from .core import PhoenixSource

_source_registry = {}


def register_source(key: str, cls: Type[PhoenixSource]):
    """Register a new source class with a given key."""
    if key in _source_registry:
        raise ValueError(f"Source '{key}' is already registered.")
    _source_registry[key] = cls


def list_sources() -> list[str]:
    """List all registered source keys."""
    return list(_source_registry.keys())


def find_source(name: str):
    """Get the source class by name."""
    try:
        return _source_registry[name]
    except KeyError:
        raise ValueError(f"Source '{name}' is not registered. Available sources: {list_sources()}")


# TODO: Implement "guess"ing logic based on directory contents
def determine_best_source(path: pathlib.Path) -> Type[PhoenixSource] | None:
    """Determine the best matching source class for the given directory path."""
    raise NotImplementedError
