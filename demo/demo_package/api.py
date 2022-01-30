from demo_package.api_version import DemoPackageAPI


@DemoPackageAPI.new(2)
def example_function(a, b):
    return a, b


@example_function.version(1)
def example_function(a):
    return a


class ExampleClass:
    # methods and static methods
    @DemoPackageAPI.new(3)
    @staticmethod
    def example_method(a, b):
        return a, b

    @example_method.version(2)
    def example_method(self, a, b):
        return a, b

    @example_method.version(1)
    def example_method(self, a):
        return a

    # method and property
    @DemoPackageAPI.new(2)
    @property
    def example_attr(self):
        return 5

    @example_attr.version(1)
    def example_attr(self):
        return 5

    @DemoPackageAPI.new(2)
    @classmethod
    def example_classmethod(cls, a):
        return cls()

    @example_classmethod.version(1)
    @classmethod
    def example_classmethod(cls):
        return cls()
