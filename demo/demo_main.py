from demo_package.api import example_function, ExampleClass
from demo_package.api_versioner import DemoPackageVersion


def main():
    cls = ExampleClass()

    print("--function demo--")
    with DemoPackageVersion(1):
        # Use the v1 api
        print("example_function v1", example_function)
        print("example_function v1 return", example_function("a"))

    with DemoPackageVersion(2):
        # Use the v2 api
        print("example_function v2", example_function)
        print("example_function v2 return", example_function("a", "b"))

    print("\n--method demo--")
    with DemoPackageVersion(1):
        # Use the v1 api
        print("example_method v1", cls.example_method)
        print("example_method v1 return", cls.example_method("a"))

    with DemoPackageVersion(2):
        # Use the v2 api
        print("example_method v2", cls.example_method)
        print("example_method v2 return", cls.example_method("a", "b"))

    with DemoPackageVersion(3):
        # Future behaviour
        print("example_method (static) v3", cls.example_method)
        print("example_method (static) v3 return", cls.example_method("a", "b", "c"))

    print("\n--class method demo--")
    with DemoPackageVersion(1):
        # Use the v1 api
        print("example_classmethod v1", cls.example_classmethod)
        print("example_classmethod v1 return", cls.example_classmethod())

    with DemoPackageVersion(2):
        # Use the v2 api
        print("example_classmethod v2", cls.example_classmethod)
        print("example_classmethod v2 return", cls.example_classmethod("a"))

    print("\n--attr/property demo--")
    with DemoPackageVersion(1):
        # Use the v1 api
        print("example_attr v1", cls.example_attr)
        print("example_attr v1 return", cls.example_attr())
        try:
            cls.example_attr = 0
        except AttributeError as e:
            print(e)
        else:
            print("Error: Functions should not be settable")

    with DemoPackageVersion(2):
        # Use the v2 api
        print("example_attr v2 property value", cls.example_attr)
        try:
            cls.example_attr = 0
        except AttributeError as e:
            print(e)
        else:
            print("Error: Properties without a setter should not be settable")

    with DemoPackageVersion(3):
        # Future behaviour
        print("example_attr v3 property value", cls.example_attr)
        print("setting property to 10")
        cls.example_attr = 10
        print("example_attr v3 property value", cls.example_attr)


if __name__ == "__main__":
    main()
