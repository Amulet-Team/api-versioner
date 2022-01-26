# Private API
The class in core.py makes up the private API for each object.

Each class stores the data for the object and a private API and implementation.

Only the public API is able to interact with these classes

We should be able to modify these however we like as long as we update the public APIs to behave the same.

I have added "Core" to the end to make it more clear that they are not public classes

# Public API

Where possible this should just be a collection of functions with minimal actual code.

The implementations should be in the private package and this should just be a wrapper for that.

They should be exposed in the package.api package and that is where everything should import them from (even first party code)
