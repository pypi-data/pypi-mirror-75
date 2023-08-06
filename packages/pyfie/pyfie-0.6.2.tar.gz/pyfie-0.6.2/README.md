Thank you for choosing pyfie!

-----------------------------------------

Here are the (shared) things you can use:

**tile(value, password = None)**

`tile()` is a shared class, that's used to make instances that can be encrypted into files.

**write(path: str, value: tile)**

`write()` is a shared function, that tries to write an encrypted tile class instance into the file in path.

**read(path: str, password = None)**

`read()` is a shared function, which is used to (try to) return a decrypted tile class instance from the file in path.

-------------

Last changes:

* 0.6.2 - completely new system
* 0.5.6 - new files tree
* 0.5.2 - sorted things into specific files
* 0.5.1 - now pyfie is even more secure
* 0.4.8 - made the `password` argument default (as *None*)
