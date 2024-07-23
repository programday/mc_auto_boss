import functools
from typing import TypeVar

from .annotations import _Auto, get_cls_auto_before, get_cls_auto_after, RefField, _func_args_auto_params, \
    _func_kwargs_auto_params, Auto
from .containers import Container
from .error import InjectionError


def _kwargs_dependency_create(cls, fields, field_items, instance=None):
    """create kwargs dependency"""

    for field_name, field_type, field_auto in field_items:

        for auto_kw_name, ref_field in field_auto.kw_ref_fields:
            ref_field: RefField
            if instance and hasattr(instance, ref_field.name):
                field_auto.kwargs.update({auto_kw_name: getattr(instance, ref_field.name)})
            elif ref_field.name in fields:
                field_auto.kwargs.update({auto_kw_name: fields[ref_field.name]})
            else:
                raise Exception(f"Reference field {ref_field.name} not found in {cls.__module__}{cls.__name__}")

        if instance:
            for index, ref_field in field_auto.args_ref_fields:
                ref_field: RefField
                args = list(field_auto.args)
                if instance and hasattr(instance, ref_field.name):
                    args[index] = getattr(instance, ref_field.name)
                elif ref_field.name in fields:
                    args[index] = fields[ref_field.name]
                else:
                    raise Exception(f"Reference field {ref_field.name} not found in {cls.__module__}{cls.__name__}")
                field_auto.args = tuple(args)
        try:
            field_value = _object_create(field_type, field_auto)
        except Exception as e:
            raise InjectionError(e, f'Failed to inject {field_name} in {cls.__module__}.{cls.__name__}, {e}')

        fields[field_name] = field_value
    return fields


def _args_dependency_create(cls: type, kwargs: dict, field_items):
    """create args dependency"""
    for field_index, field_name, field_type, field_auto in field_items:
        for auto_kw_name, ref_field in field_auto.kw_ref_fields:
            ref_field: RefField
            if ref_field.name not in kwargs:
                raise Exception(f"Reference field {ref_field.name} not found in {cls.__module__}{cls.__name__}")
            field_auto.kwargs.update({auto_kw_name: kwargs[ref_field.name]})
        try:
            field_value = _object_create(field_type, field_auto)
        except Exception as e:
            raise InjectionError(e, f'Failed to inject {field_name} in {cls.__module__}.{cls.__name__}, {e}')
        kwargs.update({field_name: field_value})
    return kwargs


def _object_create(cls: type, auto: _Auto):
    """
    Create a class instance with auto-injected dependencies.

    Parameters:
    - cls (type): The class to create an instance of.

    Returns:
    - object: The created instance.
    """
    container = Container.__instance__
    if not container:
        raise Exception("No container instance found, please initialize a container first")

    if issubclass(cls, Container):
        return cls.__instance__

    fields = {}
    _kwargs_dependency_create(cls, fields, get_cls_auto_before(cls))
    instance = container.get_provider(cls).provide(auto)
    for field_name, field_value in fields.items():
        setattr(instance, field_name, field_value)
    _kwargs_dependency_create(cls, fields, get_cls_auto_after(cls), instance)

    for field_name, field_value in fields.items():
        setattr(instance, field_name, field_value)

    if hasattr(instance, '__post_init__'):
        instance.__post_init__()
    return instance


def _get_patched(fn):
    @functools.wraps(fn)
    def _patched(*args, **kwargs):
        args_auto_params = list(_func_args_auto_params(fn))
        _args_dependency_create(fn, kwargs, args_auto_params)
        kwargs_auto_params = list(_func_kwargs_auto_params(fn))
        _kwargs_dependency_create(fn, kwargs, kwargs_auto_params)
        return fn(*args, **kwargs)

    return _patched


def inject(fn):
    """
    Function decorator that injects dependencies into function parameters.

    Parameters:
    - fun (function): The function to decorate.

    Returns:
    - function: The decorated function.
    """

    return _get_patched(fn)


def object_create(cls: type, auto: _Auto = Auto()):
    """
    Create a class instance with auto-injected dependencies.

    Parameters:
    - cls (type): The class to create an instance of.

    Returns:
    - object: The created instance.
    """
    return _object_create(cls, auto)


_T = TypeVar('_T')


def inject_object(cls: type[_T], auto: _Auto = Auto()) -> _T:
    return object_create(cls, auto)
