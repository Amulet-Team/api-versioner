from demo_package.api import example_function, ExampleClass
from demo_package.api_version import DemoPackageLibraryVersion


def main():
    cls = ExampleClass()

    with DemoPackageLibraryVersion(1):
        # Use the v1 api
        print("example_function v1", example_function)
        print("example_function v1 return", example_function("a"))
        print("example_method v1", cls.example_method)
        print("example_method v1 return", cls.example_method("a"))
        print("example_attr v1", cls.example_attr)
        print("example_attr v1 return", cls.example_attr())
        print("example_classmethod v1", cls.example_classmethod)
        print("example_classmethod v1 return", cls.example_classmethod())

    with DemoPackageLibraryVersion(2):
        # Use the v2 api
        print("example_function v2", example_function)
        print("example_function v2 return", example_function("a", "b"))
        print("example_method v2", cls.example_method)
        print("example_method v2 return", cls.example_method("a", "b"))
        print("example_attr v2", cls.example_attr)
        print("example_attr v2 property value", cls.example_attr)
        print("example_classmethod v2", cls.example_classmethod)
        print("example_classmethod v2 return", cls.example_classmethod("a"))

    with DemoPackageLibraryVersion(3):
        # Future behaviour
        print("example_method v3", cls.example_method)
        print("example_method v3 return", cls.example_method("a", "b"))


if __name__ == "__main__":
    main()
