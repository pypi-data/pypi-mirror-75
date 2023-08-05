import os
from pathlib import Path
from typing import Any, Final, Iterator, Literal, MutableMapping, TypedDict, cast

import yaml

from .os import safe_create

ConfigKey = Literal["org"]


def sym_config_file(file_name: str) -> Path:
    try:
        xdg_config_home = Path(os.environ["XDG_CONFIG_HOME"])
    except KeyError:
        xdg_config_home = Path.home() / ".config"
    sym_config_home = xdg_config_home / "sym"
    return sym_config_home / file_name


class ConfigSchema(TypedDict, total=False):
    org: str


class Config(MutableMapping[ConfigKey, Any]):
    __slots__ = ["path", "config"]

    path: Final[Path]
    config: Final[ConfigSchema]

    def __init__(self) -> None:
        self.path = sym_config_file("config.yml")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open() as f:
                config = cast(ConfigSchema, yaml.safe_load(stream=f))
        except FileNotFoundError:
            config = ConfigSchema()
        self.config = config

    def __flush(self) -> None:
        with safe_create(self.path) as f:
            yaml.safe_dump(self.config, stream=f)

    def __getitem__(self, key: ConfigKey) -> Any:
        return self.config[key]

    def __delitem__(self, key: ConfigKey) -> None:
        del self.config[key]
        self.__flush()

    def __setitem__(self, key: ConfigKey, value: Any) -> None:
        self.config[key] = value
        self.__flush()

    def __iter__(self) -> Iterator[ConfigKey]:
        return cast(Iterator[ConfigKey], iter(self.config))

    def __len__(self) -> int:
        return len(self.config)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path})"

    def get_org(self) -> str:
        return self.config["org"]
