import enum
import inspect
from typing import Iterable, Type


class FillEnum(object):

    """This Decorator returns an Enum, which contains all values in `values`.

    Values, which the passed class not include, will be auto generated with
    `prefix` + value as name if they are in the `values` list.

    Args:
        values: An iterable list of values for the Enum members.
        enum_cls: The Enum class or a subclass of it.
        prefix: The prefix for the name of the auto generated Enum members.
        *args: Will be passed to the `enum_cls` constructor.
        **kwargs: Will be passed to the `enum_cls` constructor.

    Author:
        Fabian Raab <fabian@raab.link>
    """

    def __init__(
        self,
        values: Iterable,
        enum_cls: Type[enum.Enum] = enum.Enum,
        prefix: str = "val",
        *args,
        **kwargs,
    ):
        self.values = values
        self.enum_cls = enum_cls
        self.prefix = prefix
        self.args = args
        self.kwargs = kwargs

    def __call__(self, cls: Type[enum.Enum]):
        members = []
        cls_values = set()  # set of values present in `cls`

        # Copy members of passed class `cls`
        attributes = inspect.getmembers(cls)
        for attr in attributes:
            if attr[0].startswith("__") and attr[0].endswith("__"):
                continue
            cls_values.add(attr[1])
            members.append(attr)
            any_member = attr[0]  # Any arbitrary member of the new Enum

        # set members, which are in `values` and not already present in `cls`
        for value in self.values:
            if value in cls_values:
                continue
            members.append((self.prefix + str(value), value))
            any_member = self.prefix + str(value)

        new_enum_cls = self.enum_cls(
            cls.__name__, members, *self.args, **self.kwargs
        )

        # copy docstring
        getattr(new_enum_cls, any_member).__class__.__doc__ = cls.__doc__

        return new_enum_cls
