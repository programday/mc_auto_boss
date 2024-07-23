import json
from typing import Dict

import yaml

from .providers import Provider, get_provider_type

ENV_DEV = 'dev'
ENV_PROD = 'prod'


class Container:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if Container.__instance__ is None:
            Container.__instance__ = super(Container, cls).__new__(cls)
            return Container.__instance__
        elif Container.__instance__.__class__ == cls:
            return Container.__instance__
        else:
            raise Exception("Container is a singleton class, cannot be instantiated twice")

    def __init__(self, config: dict = None, config_file_path: str = None) -> None:
        self.__providers__: Dict[type, Provider] = dict()
        self._config = config or dict()
        if config_file_path:
            self._config_from_file(config_file_path)
        self._env = self._config.get('env', ENV_DEV)

        self._providers_loading()

    @property
    def config(self):
        return self._config

    @property
    def env(self):
        return self._env

    @property
    def is_dev(self):
        return self._env == ENV_DEV

    def _config_from_file(self, config_file_path: str):
        suffix = config_file_path.split('.')[-1]
        if suffix == 'json':
            self._config_from_json_file(config_file_path)
        elif suffix == 'yaml':
            self._config_from_yaml_file(config_file_path)
        else:
            raise Exception('Unsupported config file type %s, only json and yaml are supported' % suffix)

    def _config_from_dict(self, config: dict):
        self._config.update(config)
        return self

    def _config_from_json_file(self, config_file_path: str):
        with open(config_file_path, 'r') as f:
            self._config.update(json.load(f))
        return self

    def _config_from_yaml_file(self, config_file_path: str):
        with open(config_file_path, 'r') as f:
            self._config.update(yaml.safe_load(f.read()))
        return self

    def add_provider(self, provider: Provider):
        self.__providers__[provider.provides] = provider

    def _providers_loading(self):
        self._internal_loading()
        self.providers_loading()

    def _internal_loading(self):
        """
        Load internal providers.
        :return:
        """
        ...

    def providers_loading(self):
        """
        Load providers.
        Example:
            def providers_loading(self):
                config_provider(self, 'config')
        """
        ...

    def get_provider(self, cls: type):
        if cls not in self.__providers__:
            provider_type = get_provider_type(cls)
            if provider_type:
                provider = provider_type(self, cls)
                self.add_provider(provider)
            else:
                raise Exception(f"Provider not found for {cls.__module__}.{cls.__name__}")
        return self.__providers__[cls]

    def __del__(self):
        Container.__instance__ = None
        for provider in self.__providers__.values():
            provider.__del__()
        self.__providers__.clear()
        self._config.clear()
