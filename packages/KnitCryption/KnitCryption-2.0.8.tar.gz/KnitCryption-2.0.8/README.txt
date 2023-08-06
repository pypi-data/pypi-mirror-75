KnitCryption Documentation and how-to

KnitCryption/KnitCrypter is intended to make encrypting files/strings/data
simpler and less of a hassle. Still a constant work in progress, It's not the
end of the world is something is 'missing' from the overall project.

There are some basics to go over first, these are the main tools KnitCrypter has
to offer.

knitpattern; a knitpattern object requires a minimum of two arguments but has the
following available:

    1. string; a string of unique characters which will be refrenced for 
    assignment. It is recommended to utilize the string library to produce all
    available characters. This is done so that the user can define thier own
    sequence.

    2. base; this is the base type a knitpattern object will utilize to generate
    numerical assignment values. At this current time, it only accepts 2-10 or
    hex and oct as appropriate base types, but RND is looking into expanding the
    functionality.

    3. func; by default, there is a function already in place that just returns
    the current value of iteration, but is left as a keyword that the user may
    implement thier own values to assignment. e.g. 'lambda x,y: x**y' where 'x'
    is already defined by the generator and any 'args' passed into the
    knitpattern object will be passed into the following arguments of the 
    function.

If a sequence does not return with any equivalent, a successful knitpattern
object will be created! Congrats! After a new object is created, it will have
the following attributes available:

    1. prefix; the prefix property will return the base type of the object in
    string form. e.g. 'hex' returns '0x' or 'base 6' returns '6b'.

    2. sequence; the sequence property returns a dict object after calling a 
    sub-property of either 'from_keys' or 'from_values'. 'from_keys' returns 
    the original dictionary where the keys are-- go figure --the keys of the
    new dictionary object, 'from_values' being the inverse and returning a dict
    object where the values are the head of the new dict object.

knitpattern objects allow the user to get thier total length directly from 
calling 'len(knitpattern)' but is not immediately iterable. Instead use the
sequence property to iterate through a knitpattern object.

Overall, a knitpattern object would be instantiated, like this:
>>> assignment = lamda x,y: y**x
>>> my_key = knitpattern('abcdefg...',hex,assignment,3)

knitcrypt; a knitcrypt object is a context manager to allow encrypting entire
files from a knitpattern object. A knitcrypt object requires a minimum of two
arguments but has the following available:

    1. path; the file path knitcrypt is supposed to look for, and open for
    modification.

    2. pattern; the knitpattern object which will utilize it's sequence to
    either encrypt or decrypt a file

    3. encoding; by default, the encoding is set to 'UTF-8' but has been added
    to allow the user to either change the encoding manually or read different
    files.

Upon entry of a knitcrypt object, a new _File_Struct is created which opens the
desired file. When a _File_Struct object is created, it will have the following
attributes available for encrypting/decrypting:

    1. contents; this property allows the user to view the contents that were
    read from the file prior to writing the file again.

    2. stitch; temporarily creates a _Needle_Struct as a _Stitch_Struct. Like
    the name suggests, it's intended purpose is to allow the user the ability to
    encrypt either all or specified lines of the contents.

    3. unknit; temporarily creates a _Needle_Struct as an _Unknit_Struct. It's
    intended purpose is to allow the user the ability to decrypt all or 
    specified lines of the contents.

    4. close; writes the contents back onto the file, then closes the 
    connection.

A _Needle_Struct, while not directly available is an integral part of the
KnitCryption process. When calling on the _File_Struct object for modification,
a _Needle_Struct (such as stitch or unknit) currently has two attributes 
available to the user:

    1. from_lines; specifies the range of desired lines to be modified.

    2. all_lines; modifies all lines found inside of the _File_Struct contents.

    3. stamp_contents; appends a stamp stating that the file has been encrypted.

    4. erase_stamp; verifies first that a stamp has been added to the end of the
    file contents, then removes it if it does.

Before a knitcrypt object exits, it will call the _File_Struct object's close
method to finalize the modification.

Overall a knitcrypt object should be instantiated like so:
>>> with knitcrypt('.\somepath', my_key) as blanket:
>>>     blanket.stitch.all_lines()
>>>     blanket.stitch.stamp_contents()