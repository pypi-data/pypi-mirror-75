# libqtum
[![GitHub license][license-image]][license-url]
[![PyPI Version][pypi-image]][pypi-url]

<!-- Badges -->
[license-image]: https://img.shields.io/github/license/ivanovart/fill_enum?style=flat-square
[license-url]: https://github.com/ivanovart/fill_enum/blob/master/LICENSE
[pypi-image]: https://img.shields.io/pypi/v/fill_enum?style=flat-square
[pypi-url]: https://pypi.org/project/fill_enum/

This Decorator returns an Enum, which contains all values in `values`.

Values, which the passed class not include, will be auto generated with
`prefix` + value as name if they are in the `values` list.

Args:
    values: An iterable list of values for the Enum members.
    enum_cls: The Enum class or a subclass of it.
    prefix: The prefix for the name of the auto generated Enum members.
    *args: Will be passed to the `enum_cls` constructor.
    **kwargs: Will be passed to the `enum_cls` constructor.

[Gitlab Snippet](https://gitlab.com/snippets/5976)

[Original Blog Post](https://bubblesorted.raab.link/content/automatically-fill-missing-values-python-enum#simple-table-of-contents-1)
