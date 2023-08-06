Thank you for choosing pyfie!

------------------------------------------

Here are the (shared) methods you can use:

**compose(path: str, value, password)**

`compose()` is a function used to create files with an encrypted value. Sets the password for this (hopefully) unique path as given.

**parse(path: str, password)**

`parse()` is a function used to get decrypted value of a file, but first, given password must match with the set one.

------------------------------------------------------------------------------------------------------------------------------------------

In update *this* I have completely rewrote the way, that pyfie encrypts and decrypts files. That's why the structure of functions changed.

Now, it uses pickle module and classes, with a simple idea of passwords. 

-------------

Last changes:

* 0.4.8 - made the `password` argument default (as *None*)
