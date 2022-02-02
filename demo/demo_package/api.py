from typing import Tuple, Any, Callable
from demo_package.api_versioner import api_version


@api_version(1)
def example_function(a):
    """
    Example function API V1

    :param a: Input a
    :return: Returns all inputs
    """
    return a


@api_version(2)
def example_function(a, b):
    """
    Example function API V2

    :param a: Input a
    :param b: Input b
    :return: Returns all inputs
    """
    return a, b


class ExampleClass:
    def __init__(self):
        self.var = 5

    # methods and static methods
    example_method: Callable[[Any, Any, Any], Tuple[Any, Any, Any]]

    @api_version(1)
    def example_method(self, a):
        """
        Example method API V1.

        :param a: Input a
        :return: Returns all inputs
        """
        return a

    @api_version(2)
    def example_method(self, a, b):
        """
        Example method API V2.

        :param a: Input a
        :param b: Input b
        :return: Returns all inputs
        """
        return a, b

    @api_version(3)
    @staticmethod
    def example_method(a, b, c):
        """
        Example method API V3. This one is a staticmethod

        :param a: Input a
        :param b: Input b
        :param c: Input c
        :return: Returns all inputs
        """
        return a, b, c

    # method and property

    @api_version(1)
    def example_attr(self):
        """
        Example attribute. The future API versions change this to a property
        """
        return self.var

    @api_version(2)
    @property
    def example_attr(self):
        """
        Example property. This property does not have a setter
        """
        return self.var

    @api_version(3)
    @property
    def example_attr(self):
        """
        Example property API V3. This is a property getter
        Returns the var attribute
        """
        return self.var

    @example_attr.setter
    def example_attr(self, example_attr):
        """
        Setter method for the API V3 property.
        """
        self.var = example_attr

    # Class method
    example_classmethod: Callable[[Any], "ExampleClass"]

    @api_version(1)
    @classmethod
    def example_classmethod(cls):
        """
        Example class method

        :return: Instance of this class
        """
        return cls()

    @api_version(2)
    @classmethod
    def example_classmethod(cls, a):
        """
        Example class method

        :param a: Input a
        :return: Instance of this class
        """
        return cls()
