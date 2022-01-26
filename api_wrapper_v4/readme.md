This is the v3 example with some changes:

- Modified the private get_chunk implementation to wrap the data rather than letting the API handle it. This minimises the core class exposure
- The factory class is now merely a validator for the API classes so renamed and modified it to better suit its purpose.
