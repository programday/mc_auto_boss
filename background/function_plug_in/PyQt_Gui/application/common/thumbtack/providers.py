import abc
import threading
import warnings
from typing import Dict, Generic, TypeVar, Tuple

from .annotations import Auto
from .error import ProvideError

ATTRIBUTE_PROVIDER = '__provider__'
ATTRIBUTE_CONFIG = '__inject_config__'

_T = TypeVar('_T')


class Provider(Generic[_T], abc.ABC):
    """
    Abstract base class for providers of objects.
    """

    __inject_config__: str = None

    def __init__(self, container, provides: type[_T], ref_config: str = None, *args, **kwargs):
        """
        Initialize a Provider instance.

        Parameters:
        - container (Container): The container that this provider belongs to.
        - provides (type): The type of object that this provider can provide.
        - ref_config (str, optional): The name of the configuration to inject.
        - config_kwargs (dict, optional): Additional keyword arguments for configuration.
        - args (tuple, optional): Positional arguments for providing the object.
        - kwargs (dict, optional): Keyword arguments for providing the object.
        """
        self._container = container
        self._provides = provides
        self._args = args or tuple()
        self._kwargs = kwargs or dict()
        self._ref_config = ref_config
        self._container.add_provider(self)

    @property
    def container(self):
        """
        Get the container that this provider belongs to.

        Returns:
        - Container: The container that this provider belongs to.
        """
        return self._container

    @property
    def args(self) -> tuple:
        return self._args

    @property
    def kwargs(self) -> dict:
        return self._kwargs

    @property
    def provides(self) -> type:
        """
        Get the type of object that this provider can provide.

        Returns:
        - type: The type of object that this provider can provide.
        """
        return self._provides

    @abc.abstractmethod
    def _provide(self, args: tuple, kwargs: dict):
        """
        Abstract method for providing an object. Subclasses must implement this method.

        Parameters:
        - args: Positional arguments for providing the object.
        - kwargs: Keyword arguments for providing the object.
        """
        ...

    @property
    def config(self):
        config = dict()
        ref_config = self._ref_config or getattr(self._provides, ATTRIBUTE_CONFIG, None) or self.__inject_config__
        if ref_config:
            _inject_config = self.container.config.get(ref_config)
            if _inject_config:
                config.update(_inject_config)
        return config

    def provide(self, auto: Auto = None) -> _T:
        """
        Provide an object using the stored arguments and keyword arguments.

        Parameters:
        - auto (Auto): An Auto instance containing arguments and keyword arguments.

        Returns:
        - object: The provided object.
        """
        config = self.config

        kwargs = dict()
        kwargs.update(self._kwargs)
        kwargs.update(config)
        if auto:
            args = auto.args or self._args
            kwargs.update(auto.kwargs)
        else:
            args = self._args
        instance = self._provide(args, kwargs)
        return instance

    def __del__(self):
        pass


_providers_types: Dict[type, type[Provider]] = {}


def get_provider_type(cls: type):
    """
    Get a provider for the given class.
    If cls metaclass is SingletonMeta, return Singleton.

    Parameters:
    - cls (type): The class for which to get a provider.

    Returns:
    - Provider: The provider for the given class. If no provider is found, return Factory or Singleton.
    """
    provider_type = _providers_types.get(cls, None)
    if provider_type:
        return provider_type
    provider_type = getattr(cls, ATTRIBUTE_PROVIDER, None)

    if provider_type:
        if not issubclass(provider_type, Provider):
            warnings.warn(f'{cls.__module__}.{cls.__name__}.__provider__ must be a subclass of Provider',
                          DeprecationWarning)
        else:
            return provider_type

    if type(cls) == SingletonMeta:
        return Singleton
    else:
        return Factory


def config_provider(cls: type, provider_type: type[Provider]):
    """
    Set a provider for the given class.

    Parameters:
    - cls (type): The class for which to set a provider.
    - provider (ProviderType): The provider for the given class.
    """
    _providers_types[cls] = provider_type


_global_lock = threading.Lock()
_locks: Dict[type, threading.RLock] = {}


def _get_provide_rlock(provide: type) -> threading.RLock:
    """
    Get a reentrant lock for the given id.
    :param provide:
    :return: 
    """

    with _global_lock:
        if provide not in _locks:
            _locks[provide] = threading.RLock()
        return _locks[provide]


class Factory(Provider[_T]):
    def _provide(self, args: tuple, kwargs: dict):

        try:
            return self.provides(*args, **kwargs)
        except Exception as e:
            raise ProvideError(e, f'Failed to provide {self.provides.__module__}.{self.provides.__name__}, {e}')


class MultiFactory(Factory[_T]):

    def provide(self, auto: Auto = None) -> _T:

        if not Auto:
            raise ValueError('Auto is required for MultiProvider')
        auto_copy = auto.__copy__()

        if len(auto_copy.args) < 1:
            raise ValueError('At least one argument is required for MultiProvider')

        if not isinstance(auto_copy.args[0], str):
            raise ValueError('The first argument of MultiProvider must be a string')
        config = self.config[auto_copy.args[0]]
        auto_copy.args = auto_copy.args[1:]
        kwargs = dict()
        kwargs.update(self._kwargs)
        kwargs.update(config)
        args = auto_copy.args or self._args
        kwargs.update(auto_copy.kwargs)
        instance = self._provide(args, kwargs)
        __post_init__ = getattr(instance, '__post_init__', None)
        if __post_init__:
            __post_init__()
        return instance


class SingletonMeta(type):
    """
    Metaclass for singleton classes.
    """
    ...


class Singleton(Factory[_T]):
    """
    Provider class for creating singleton objects.
    """

    __instances__: Dict[type, object] = {}

    def update(self, instances: _T, auto: Auto):
        """Update singleton object with auto-injected dependencies."""
        ...

    def provide(self, auto: Auto = None):

        """
        Provide a singleton object. If the object has already been created,
        return the existing instance; otherwise, create a new one.

        Parameters:
        - args: Positional arguments for providing the object.
        - kwargs: Keyword arguments for providing the object.

        Returns:
        - object: The provided singleton object.
        """
        with _get_provide_rlock(self.provides):

            if not self.__instances__.get(self.provides):
                instance = super().provide(auto)
                self.__instances__[self.provides] = instance
            else:
                instance = self.__instances__[self.provides]
                self.update(instance, auto)

            return instance

    def __del__(self):
        print(self.__instances__.pop(self.provides, None))

    @classmethod
    def clear(cls):
        cls.__instances__.clear()


class MultiSingleton(MultiFactory[_T]):
    __instances__: Dict[Tuple[type, str], object] = {}

    def update(self, instances: _T, auto: Auto):
        """Update singleton object with auto-injected dependencies."""
        ...

    def provide(self, auto: Auto = None) -> _T:
        if not Auto:
            raise ValueError('Auto is required for MultiProvider')
        auto = auto.__copy__()

        if len(auto.args) < 1:
            raise ValueError('At least one argument is required for MultiProvider')

        if not isinstance(auto.args[0], str):
            raise ValueError('The first argument of MultiProvider must be a string')

        config_name = auto.args[0]

        with _get_provide_rlock(self.provides):
            key = (self.provides, config_name)
            if not self.__instances__.get(key):
                instance = super().provide(auto)
                self.__instances__[key] = instance
            else:
                instance = self.__instances__[key]
                self.update(instance, auto)

            return instance
