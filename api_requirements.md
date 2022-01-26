### API Requirements

Our library can be used as a standalone library where the project decided which library version it wanted to use. 
That allows the calling code to use an old version of the library if we update it.
In this case standard library rules apply.

Our library is also used embedded in the editor where we decide which library version gets included.
Plugin code here cannot decide which version of the library gets used.

We are proposing solutions that will allow the current API version to be used by default.
It should also enable plugin code to specify a depreciated version of the API like a project would with a library version.

Currently we have been concentrating on classes because this is most of what plugins interact with.

### Requirements
- Class Structure
  - Classes should have a public and private side
    - The public API must be used to interact with the class
    - The private side must not be used by external code so that we can modify it at will
      - This includes attributes and optional methods
      - The public API will need updating to accommodate these changes
  - There must be a mechanism to depreciate and change the public API without breaking calling code
    - New API versions should not be limited by previous API versions
    - New API versions should be able to change the return type if it makes sense
    - Depreciated API calls should warn the user
  - It should be clear if code tries to use an API which has been removed
  - Calling code must have a mechanism to specify which API it was designed to use
    - This enables code to use a newer version of the library with support for new game versions without having to update the code
    - This allows us to release backwards compatible updates to the latest API and breaking changes as a new API allowing old code to use the depreciated API
  - There must be a way to get the object wrapped in a different API without exposing the private data
  - An object must be editable through each API simultaneously
