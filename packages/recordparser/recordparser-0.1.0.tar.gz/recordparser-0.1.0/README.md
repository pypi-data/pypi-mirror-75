# Python recordparser

Parse delimited text file into a class

## Synopsis

This module will parse a delimited text file, transforming each record
of text fields into a given class with fields and data types.
Only return records that conform to this description will be returned.

For example, given an input file like this:

```
$ cat test_data/items.csv
id_,name,price
1,foo,3.25
2,bar,.43
3,baz,4.01
```

We can create a class called `Item` to describe a record with the following 
definition:

```
from typing import NamedTuple, TextIO


class Item(NamedTuple):
    id_: int
    name: str
    price: float
```

The `recordparser.parse()` function will return a generator of records that 
will be of the type `Item`.
Various problems may cause this to fail which are currently raised
with exceptions, so use `try`/`catch`:

```
try:
    parser = recordparser.parse(fh=open('test_data/items.csv'),
                                cls=Item,
                                delimiter=',',
                                quiet=False)

    for rec in parser:
        print(rec)

except Exception as err:
    print(err)
```

This would print the following:

```
Item(id_=1, name='foo', price=3.25)
Item(id_=2, name='bar', price=0.43)
Item(id_=3, name='baz', price=4.01)
```

## Input file delimiter

The default field delimiter is a comma, but you can set the "delimiter"
to any valid character.
The `csv` module is used to parse the input text files.

## Ignore undefined fields

The source file may name columns which the given class does not describe.
Only the columns from the class will be used, so the extra fields will be
ignored.
Here the "can_discount" field is skipped:

```
$ cat test_data/extra_fields.csv
id_,name,price,can_discount
1,foo,3.25,True
2,bar,.43,False
3,baz,4.01,True
```

So the program would emit the same output:

```
Item(id_=1, name='foo', price=3.25)
Item(id_=2, name='bar', price=0.43)
Item(id_=3, name='baz', price=4.01)
```

## Modify column names

Often an input file will have column names you need to map to your class'
fields.
You can provide a "mapping" dictionary of the source name to a field name.
In this file, the columns "id," "item," and "cost" need to be mapped to "id_,"
"name," and "price," respectively:

```
$ cat test_data/other_names.csv
id,item,cost
1,foo,3.25
2,bar,.43
3,baz,4.01
```

Here is the code:

```
mapping = {'id': 'id_', 'item': 'name', 'cost': 'price'}
parser: Iterable[Item] = recordparser.parse(fh=args.file,
                                            cls=Item,
                                            mapping=mapping
                                            delimiter=args.delimiter)
```

The field will be mapped to their correct counterparts in the `Item` class:

```
Item(id_=1, name='foo', price=3.25)
Item(id_=2, name='bar', price=0.43)
Item(id_=3, name='baz', price=4.01)
```

## Parsing files without column names

If you have an input file that does not list the columns in the first
line, you can set the "fieldnames" option to pass to `csv.DictReader`.
Be sure not to pass this option to _rename_ existing columns; instead use 
the above "mapping" option.

```
$ cat test_data/no_names.csv
1,foo,3.25
2,bar,.43
3,baz,4.01
```

This is the code:

```
parser: Iterable[Item] = recordparser.parse(
    fh=args.file,
    cls=Item,
    fieldnames=['id_', 'name', 'price'])
```

To produce our familiar output:

```
Item(id_=1, name='foo', price=3.25)
Item(id_=2, name='bar', price=0.43)
Item(id_=3, name='baz', price=4.01)
```

## Failure on missing fields

If the input file is missing field definitions, the module will throw 
an exception (which may not be great):

```
$ cat test_data/missing_price.csv
id_,name
1,foo
2,bar
3,baz
```

Given the `Item` class, this file would be rejected:

```
$ ./rc.py test_data/missing_price.csv
Missing field: price
```

## Optional fields

You can use the `Optional` type to allow a field to be missing:

```
class Item(NamedTuple):
    id_: int
    name: str
    price: Optional[float]
```

And now the "price" will be `None`:

```
$ ./rc.py test_data/missing_price.csv
Item(id_=1, name='foo', price=None)
Item(id_=2, name='bar', price=None)
Item(id_=3, name='baz', price=None)
```

## Skipping data that does not match

If a record cannot be parsed according to the class definition, the 
record will be skipped and a message printed to STDERR (unless you 
pass `True` for the "quiet" option).
It's hard to see in this example (which is the point), but the "price"
of the "bar" item has a capital "O" instead of a "0":

```
$ cat test_data/bad_item.csv
id_,name,price
1,foo,3.25
2,bar,O.43
3,baz,4.01
```

If the "price" is a required (not `Optional`) field, the record will be skipped:

```
$ ./rc.py test_data/bad_item.csv
Item(id_=1, name='foo', price=3.25)
1: Cannot convert "O.43" to "<class 'float'>"
Item(id_=3, name='baz', price=4.01)
```

If the "price" is `Optional`, then the record will be present but the value
will be a `None`:

```
$ ./rc.py !$
./rc.py test_data/bad_item.csv
Item(id_=1, name='foo', price=3.25)
1: Cannot convert "O.43" to "typing.Union[float, NoneType]"
Item(id_=2, name='bar', price=None)
Item(id_=3, name='baz', price=4.01)
```

## Union types

Sometime the data in a column may be a mix of values.
In this case, you can use a `Union` type to declare the various type
_in the order you wish to try_.
For instance, we first want to try to convert "price" to a `float` and then
use `str` for a backup:

```
class Item(NamedTuple):
    id_: int
    name: str
    price: Union[float, str]
```

So that this data:

```
$ cat test_data/mixed_types.csv
id_,name,price
1,foo,3.25
2,bar,NA
3,baz,4.01
```

Will parse like so:

```
Item(id_=1, name='foo', price=3.25)
Item(id_=2, name='bar', price='NA')
Item(id_=3, name='baz', price=4.01)
```

## Base class must be NamedTuple

Your class must be derived from a `NamedTuple`.
Future versions may allow for the use of a `TypedDict`.
This means that the objects/records will be _immutable_ (which, IMHO, 
is a Good Thing).

## Motivation

I spend too much time parsing messy delimited files/Excel spreadsheets.
Often there are some values that need to be coerced to something like number.
If these values cannot be cast, I should skip the data.
So I kept writing `for` loops with `try`/`catch` to handle exceptions 
from `float(val)` and so forth.

With this module, I can _describe_ what the resulting data should look like
using a `class`.
The `recordparser` will handle missing and optional fields, multiple data 
types, and the mapping of the file's column names to the fields in my class.

Please let me know how I can improve this code!

https://github.com/kyclark/python-recordparser/issues

## Author

Ken Youens-Clark <kyclark@gmail.com>
