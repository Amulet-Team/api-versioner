# Changelog

### v2a
- Restructured v2 into modules to work out some other issues.

### v3
- Moved the public class api into the _private and exposed them in the public api.
  This will resolve some circular dependencies and keep the private classes in the _private package.
- The methodology is that everything should be implemented in _private and exposed in api

### v4
- Modified the private get_chunk implementation to wrap the data rather than letting the API handle it. This minimises the core class exposure
- The factory class is now merely a validator for the API classes so renamed and modified it to better suit its purpose.

### v5
- Renamed XAPIvY to XvY to make it look like the real object to users.
- Added a `cast_to` method to cast the API class to a different API version.
  - This is similar in concept to C casting where a class can be cast to one of its subclasses.
  - The class is an instance of AbstractX and can be cast to one of its subclasses.
