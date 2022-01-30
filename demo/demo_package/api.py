from demo_package.api_version import api_version


@api_version(2)
def example_function(a, b):
    return a, b


@example_function.api_version(1)
def example_function(a):
    return a


class ExampleClass:
    # methods and static methods
    @api_version(3)
    @staticmethod
    def example_method(a, b):
        return a, b

    @example_method.api_version(2)
    def example_method(self, a, b):
        return a, b

    @example_method.api_version(1)
    def example_method(self, a):
        return a

    # method and property
    @api_version(2)
    @property
    def example_attr(self):
        return 5

    @example_attr.api_version(1)
    def example_attr(self):
        return 5

    @api_version(2)
    @classmethod
    def example_classmethod(cls, a):
        return cls()

    @example_classmethod.api_version(1)
    @classmethod
    def example_classmethod(cls):
        return cls()
