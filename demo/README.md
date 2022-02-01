# Demo

This is a demonstration of the api_versioner library.

## demo_package
demo_package is a minimal package showing off the features of the library and how to go about setting it up.

You will need to specify a library version somewhere.
This is usually done in the [\_\_init\_\_.py file](demo_package/__init__.py)

You will then need to set up a ContextVar storing the library version (it is advised you default to the current library major version.)
You will then need to set up subclasses of the abstract APIManager and Version classes passing in the ContextVar that was just created and the current library version.
An example of this can be found in the [demo_package/api_versioner.py file](demo_package/api_versioner.py)

Once that is done you are free to write your APIs.
Write these like normal and put the api_version decorator on top of the function/method.
Each function/method can have multiple versions each tied to a different API version.
When the function is called or the class attribute is acquired the library will serve up the implementation for the version that is stored in the ContextVar for that context.

This library is compatible with other decorators just make sure our decorator is on top.
It has been tested with @property, @classmethod and @staticmethod and should work with custom decorators as long as the decorator exposes the `__module__`, `__qualname__` and `__name__` attributes from the original function.
This can be done easily with functools [update_wrapper](https://docs.python.org/3/library/functools.html#functools.update_wrapper) or [wraps](https://docs.python.org/3/library/functools.html#functools.wraps).

The library allows switching behaviour as well as inputs and outputs between versions.
There may be cases where you have a method that you would like to change to a property.
This library allows the same name to serve up a method to one API version and a property to another.

An example API can be found in the [demo_package/api.py file](demo_package/api.py) which shows off most of the features mentioned.

## demo_main.py
[demo_main.py](demo_main.py) is an example of how the different versions of the API would be used.
The version context manager is used to set the API version which persists until the block is exited at which point it is reset to the previous value.
The context manager also supports being nested if more than one API version is required however it is advised to use the latest version of the API.
