This is the v2a example with some changes:

- Moved the public class api into the _private and exposed them in the public api.
  This will resolve some circular dependencies and keep the private classes in the _private package.
- The methodology is that everything should be implemented in _private and exposed in api
