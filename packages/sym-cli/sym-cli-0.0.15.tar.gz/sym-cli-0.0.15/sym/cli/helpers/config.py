import os
from datetime import datetime
from pathlib import Path
from typing import Any, Final, Iterator, Literal, MutableMapping, TypedDict, cast

import yaml
from frozendict import frozendict

from .os import safe_create

ConfigKey = Literal["org", "email"]


def sym_config_file(file_name: str) -> Path:
    try:
        xdg_config_home = Path(os.environ["XDG_CONFIG_HOME"])
    except KeyError:
        xdg_config_home = Path.home() / ".config"
    sym_config_home = xdg_config_home / "sym"
    return sym_config_home / file_name


class SymConfigFile:
    def __init__(self, file_name: str):
        self.path = sym_config_file(file_name)

    def __enter__(self):
        self.file = safe_create(self.path)
        return self.file.__enter__()

    def __exit__(self, type, value, traceback):
        self.file.__exit__(type, value, traceback)

    def __str__(self):
        return str(self.path)

    def put(self, s: str):
        with self as f:
            f.write(s)


class ServerConfigSchema(TypedDict):
    last_connection: datetime


class ConfigSchema(TypedDict, total=False):
    org: str
    email: str
    default_resource: str
    servers: MutableMapping[str, ServerConfigSchema]


class Config(MutableMapping[ConfigKey, Any]):
    __slots__ = ["path", "config"]

    path: Final[Path]
    config: Final[ConfigSchema]

    def __init__(self) -> None:
        self.path = sym_config_file("config.yml")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open() as f:
                config = cast(ConfigSchema, yaml.safe_load(stream=f) or {})
        except FileNotFoundError:
            config = ConfigSchema()
        self.config = config

    def __flush(self) -> None:
        with safe_create(self.path) as f:
            yaml.safe_dump(self.config, stream=f)

    def __getitem__(self, key: ConfigKey) -> Any:
        item = self.config[key]
        if isinstance(item, dict):
            return frozendict(item)
        return item

    def __delitem__(self, key: ConfigKey) -> None:
        del self.config[key]
        self.__flush()

    def __setitem__(self, key: ConfigKey, value: Any) -> None:
        if isinstance(value, frozendict):
            value = dict(value)
        self.config[key] = value
        self.__flush()

    def __iter__(self) -> Iterator[ConfigKey]:
        return cast(Iterator[ConfigKey], iter(self.config))

    def __len__(self) -> int:
        return len(self.config)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path})"

    @classmethod
    def instance(cls) -> "Config":
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", cls())
        return getattr(cls, "__instance")

    @classmethod
    def get_org(cls) -> str:
        return cls.instance()["org"]

    @classmethod
    def get_email(cls) -> str:
        return cls.instance()["email"]

    @classmethod
    def get_servers(cls) -> str:
        return cls.instance().get("servers", frozendict())

    @classmethod
    def get_instance(cls, instance: str) -> str:
        return cls.get_servers().get(instance, ServerConfigSchema())

    @classmethod
    def touch_instance(cls, instance: str, error: bool = False):
        instance_config = cls.get_instance(instance)
        instance_config["last_connection"] = None if error else datetime.now()
        cls.instance()["servers"] = cls.get_servers().copy(
            **{instance: instance_config}
        )
