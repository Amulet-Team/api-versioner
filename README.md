# API Versioner

A small library to help maintain multiple different API versions within the same version of a library.

This library is compatible with threading and asyncio where each operation can independently specify the API version.

### Reasoning

Normally the API of a library is tied to the version of the library.
The calling code can choose which version of a library it wants to install and with that the version of the API it wants to use.

We wrote this because our library is used by third party plugin code as part of a larger application.
The plugin cannot choose which library version is used and will immediately break if we release a breaking change.

The idea of this library is to allow multiple versions of an API to coexist within a single version of the library without any limitations.
The calling code can specify the API version that it requires and the library will serve up that version of the API.

### Implementation
At its core this is implemented using a global variable from which the library will serve up the requested implementation.

The global variable is a [ContextVar](https://docs.python.org/3/library/contextvars.html) which allows each thread and asyncio context to have its own state.

To massively simplify the API implementation a decorator has been added to specify which API version the implementation is part of.
The decorator wraps up all the implementations into a class which abstracts away the switching logic and serves up the required implementation at runtime.
This means that the API only contains the implementation logic and none of the more complex switching logic.

Switching the API version is implemented using a context manager which switches back the API version when finished.

An example API and usage can be seen below.
For a more extensive demo see [the demo](demo)

```python
# api.py
from demo_package.api_versioner import api_version


@api_version(2)
def example_function(a, b):
    """
    Example function API V2

    :param a: Input a
    :param b: Input b
    :return: Returns all inputs
    """
    return a, b


@api_version(1)
def example_function(a):
    """
    Example function API V1

    :param a: Input a
    :return: Returns all inputs
    """
    return a


class ExampleClass:
    def __init__(self):
        self.var = 5

    # methods and static methods
    @api_version(2)
    def example_method(self, a, b):
        """
        Example method API V2.

        :param a: Input a
        :param b: Input b
        :return: Returns all inputs
        """
        return a, b

    @api_version(1)
    def example_method(self, a):
        """
        Example method API V1.

        :param a: Input a
        :return: Returns all inputs
        """
        return a

    # method and property
    @api_version(3)
    @property
    def example_attr(self):
        """
        Example property API V2.
        Returns the var attribute
        The API V1 implementation was a method.
        This switches it to a property but the V1 implementation is also accessible if enabled.
        """
        return self.var

    @example_attr.setter
    def example_attr(self, example_attr):
        """
        Setter method for the API V2 property.
        """
        self.var = example_attr

    @api_version(1)
    def example_attr(self):
        """
        Example attribute. The future API versions change this to a property
        """
        return self.var
```

```python
from demo_package.api_versioner import DemoPackageVersion
from demo_package.api import example_function, ExampleClass

cls = ExampleClass()

with DemoPackageVersion(1):
    print("example_function v1", example_function)
    print("example_function v1 return", example_function("a"))
    print("example_method v1", cls.example_method)
    print("example_method v1 return", cls.example_method("a"))
    print("example_attr v1", cls.example_attr)
    print("example_attr v1 return", cls.example_attr())
with DemoPackageVersion(2):
    print("example_function v2", example_function)
    print("example_function v2 return", example_function("a", "b"))
    print("example_method v2", cls.example_method)
    print("example_method v2 return", cls.example_method("a", "b"))
with DemoPackageVersion(3):
    # The library is currently on version 2 so version 3 is future behaviour
    # The future version should only be used internally and when ready the
    # library major version incremented to make it the default behaviour. 
    print("example_attr v3 property value", cls.example_attr)
    print("setting property to 10")
    cls.example_attr = 10
    print("example_attr v3 property value", cls.example_attr)
```

```
example_function v1 <demo_package.api_versioner.DemoPackageAPIManager object at 0x000001D3082328C0>
example_function v1 return a
example_method v1 <bound method ExampleClass.example_method of <demo_package.api.ExampleClass object at 0x000001D308237F10>>
example_method v1 return a
example_attr v1 <bound method ExampleClass.example_attr of <demo_package.api.ExampleClass object at 0x000001D308237F10>>
example_attr v1 return 5

example_function v2 <demo_package.api_versioner.DemoPackageAPIManager object at 0x000001D3082328C0>
example_function v2 return ('a', 'b')
example_method v2 <bound method ExampleClass.example_method of <demo_package.api.ExampleClass object at 0x000001D308237F10>>
example_method v2 return ('a', 'b')

example_attr v3 property value 5
setting property to 10
example_attr v3 property value 10
```
