import copy
import inspect
from typing import Generic, TypeVar, Type, get_type_hints, Annotated, get_origin

T = TypeVar('T')


class Annotation(object):
    """Base class for annotations."""
    ...


class RefField(Generic[T], Annotation):
    """RefField annotation for referencing a field of the same object.
    It can only be used in (AutoLazy, AutoAfter) annotations.

    Example:
        >>> class A:
        >>>     pass
        >>> class B:
        >>>     def __init__(self, a: A):
        >>>         self.a = a
        >>> class C:
        >>>     a: A = Auto()
        >>>     b: B = AutoAfter(a=RefField('a'))
    """

    def __init__(self, ref: str):
        self._name = ref

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class _Auto(Annotation):
    """Auto annotation for auto-injection of dependencies."""

    def __init__(self, *args, **kwargs):
        """
        Args:
            args: Injected positional arguments
            kwargs: Injected keyword arguments
        """

        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = dict()

        self._args = args
        self._kwargs = kwargs

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value

    def __repr__(self):
        return f"{self.__class__.__name__}(*{self.args}, **{self.kwargs})"

    @property
    def kw_ref_fields(self):
        return list(_kwargs_ref_fields(**self.kwargs))

    @property
    def args_ref_fields(self):
        return list(_args_ref_fields(*self.args))

    def __copy__(self):
        args = copy.copy(self.args)
        kwargs = copy.copy(self.kwargs)
        return self.__class__(*args, **kwargs)


_AUTO_T = TypeVar('_AUTO_T', bound=_Auto)


class Auto(_Auto):
    """Auto annotation for auto-injection of dependencies."""
    ...


class AutoBefore(_Auto):
    """AutoBefore annotation for auto-injection of dependencies before __post_init__."""
    ...


class AutoAfter(_Auto):
    """AutoAfter annotation for auto-injection of dependencies after __post_init__."""
    ...


# class AutoLazy(_Auto):
#     ...


def _kwargs_ref_fields(**kwargs):
    """Get all RefField instances from keyword arguments."""
    for field_name, field_value in kwargs.items():
        if isinstance(field_value, RefField):
            yield field_name, field_value


def _args_ref_fields(*args):
    """Get all RefField instances from keyword arguments."""
    for index, field_value in enumerate(args):
        if isinstance(field_value, RefField):
            yield index, field_value


def _get_auto_fields(cls: Type):
    """Get all auto fields from a class."""
    field_items = get_type_hints(cls, include_extras=True).items()
    for field_name, field_type in field_items:
        field_value = getattr(cls, field_name, None)
        if isinstance(field_value, _Auto):
            yield field_name, field_type, field_value
        elif get_origin(field_type) == Annotated:
            for annotation in field_type.__metadata__:
                if isinstance(annotation, _Auto):
                    yield field_name, field_type.__origin__, annotation
                    break


def _auto_fields(field_items, *auto_types: Type[_Auto]):
    """Get all auto fields of a specific type from a list of field items."""
    for field_name, field_type, field_value in field_items:
        if isinstance(field_value, auto_types):
            yield field_name, field_type, field_value


def cls_auto_fields(cls: type):
    """Get all auto fields from a class."""
    return list(_get_auto_fields(cls))


def get_cls_auto_before(cls: type):
    """Get all auto before fields from a list of field items."""
    return list(_auto_fields(_get_auto_fields(cls), Auto, AutoBefore))


def get_cls_auto_after(cls: type):
    """Get all auto after fields from a list of field items."""
    return list(_auto_fields(_get_auto_fields(cls), AutoAfter))


# def get_cls_auto_lazy(cls):
#     """Get all auto lazy fields from a list of field items."""
#     return list(_auto_fields(_get_auto_fields(cls), AutoLazy))


def _func_kwargs_auto_params(func):
    signature = inspect.signature(func)
    for parameter_name, parameter in signature.parameters.items():
        if parameter.default is not inspect.Parameter.empty:
            if isinstance(parameter.default, _Auto):
                if parameter.annotation is inspect.Parameter.empty:
                    raise TypeError(f"Auto field {parameter_name} of function {func.__module__}.{func.__name__} has no "
                                    f"type annotation")
                yield parameter_name, parameter.annotation, parameter.default
            elif get_origin(parameter.annotation) is Annotated:
                for annotation in parameter.annotation.__metadata__:
                    if isinstance(annotation, _Auto):
                        yield parameter_name, parameter.annotation.__origin__, annotation
                        break


def _func_args_auto_params(func):
    signature = inspect.signature(func)
    is_auto = False
    for index, item in enumerate(signature.parameters.items()):
        parameter_name, parameter = item
        if parameter.default is inspect.Parameter.empty and is_auto and get_origin(parameter.annotation) is not Annotated:
            raise TypeError(f"Auto field {parameter_name} of function {func.__module__}.{func.__name__}, Auto field "
                            f"must come last in args")

        if parameter.default is inspect.Parameter.empty and get_origin(parameter.annotation) is Annotated:
            for annotation in parameter.annotation.__metadata__:
                if isinstance(annotation, _Auto):
                    is_auto = True
                    yield index, parameter_name, parameter.annotation.__origin__, annotation
                    break
