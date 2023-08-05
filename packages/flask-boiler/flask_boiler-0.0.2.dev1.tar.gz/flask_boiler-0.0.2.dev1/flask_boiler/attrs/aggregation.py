from typing import Any

from marshmallow.utils import get_value

from .attribute import PropertyAttribute, _ATTRIBUTE_STORE_NAME
from ..common import _NA


class Accumulator:

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(self, value=None):
        self.value = value


class Aggregation(PropertyAttribute):
    """
    Used to aggregate multiple rows in a table to a single row
    """

    def __create_accumulator__(self, instance, value):
        inner = getattr(instance, _ATTRIBUTE_STORE_NAME)
        setattr(inner, self.name, self.f_create_accumulator(instance, value))

    def __init__(self, import_default=_NA, **kwargs):
        """ Never initialize; always set

        :param kwargs:
        """

        """
        Getter: returns accumulator
        """
        def fget(_self) -> Accumulator:
            inner = getattr(_self, _ATTRIBUTE_STORE_NAME)
            return getattr(inner, self.name)

        """
        Setter: creates accumulator
        """
        def fset(_self, value):
            self.__create_accumulator__(_self, value)

        """
        Deleter: deletes accumulator
        """
        def fdel(_self):
            inner = getattr(_self, _ATTRIBUTE_STORE_NAME)
            return delattr(inner, self.name)

        super().__init__(
            initialize=False,
            import_enabled=True,
            import_default=import_default,
            fget=fget,
            fset=fset,
            fdel=fdel,
            **kwargs
        )

        def create_accumulator(_self, value=_NA):
            return Accumulator.create(value=value)

        self.f_create_accumulator = create_accumulator

        def f_accumulate(_self):
            raise NotImplementedError

        self.f_accumulate = f_accumulate

    def create_accumulator(self, f_create_accumulator):
        self.f_create_accumulator = f_create_accumulator

    def accumulate(self, f_accumulate):
        self.f_accumulate = f_accumulate

