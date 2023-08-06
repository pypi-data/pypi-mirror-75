"""
recordparser

Parse a delimited text file into records of a given class
converting the types to those described by the class.

https://github.com/kyclark/python-recordparser

Author : Ken Youens-Clark <kyclark@gmail.com>
"""

import csv
import sys
import typing


# --------------------------------------------------
def parse(cls: typing.Type,
          fh: typing.TextIO,
          delimiter: str = ',',
          mapping: typing.Optional[typing.Dict[str, str]] = None,
          fieldnames: typing.Optional[typing.List[str]] = None,
          quiet: bool = False) -> typing.Iterable[typing.Any]:
    """
    Create a parser

    Required arguments:

    * cls (Type): The class into which each record will be cast
    * fh (TextIO): An open file handle to pass to csv.DictReader

    Options:

    * delimiter (str): The field separator for the csv module, default ','
    * fieldnames (List[str]): To use when the input file has no headers
    * mapping (Dict[str, str]): To rename existing fields
    * quiet (bool): Do not emit warnings to STDERR (default False)

    Returns:

    A generator/iterable of objects of the type "cls"

    """

    kwargs: typing.Dict[str, typing.Any] = {'delimiter': delimiter}
    if fieldnames:
        kwargs['fieldnames'] = fieldnames

    reader = csv.DictReader(fh, **kwargs)

    # Handle the mapping of src to dest fields
    if mapping:
        if flds := reader.fieldnames:
            for src, dest in mapping.items():
                if src in flds:
                    idx = flds.index(src)
                    flds[idx] = dest

            reader.fieldnames = flds

    fields = cls._field_types
    req_flds = [
        name for name, typ in fields.items()
        if (typing.get_origin(typ) is None) or (
            type(None) not in typing.get_args(typ))
    ]
    opt_flds = [
        name for name, typ in fields.items()
        if type(None) in typing.get_args(typ)
    ]

    if flds := reader.fieldnames:
        if missing := [name for name in req_flds if name not in flds]:
            raise Exception(f'Missing field: {", ".join(missing)}')

    def warn(msg):
        """Print message to STDERR"""

        if not quiet:
            print(msg, file=sys.stderr)

    for row_num, row in enumerate(reader):
        rec: typing.Dict = {}
        for fld_name, fld_type in fields.items():
            # Handle optional fields
            if fld_name not in row:
                rec[fld_name] = None
                continue

            # Try to convert raw values
            raw_val = row[fld_name]
            val = None

            # Handle Union types
            if typing.get_origin(fld_type) is typing.Union:
                for typ in typing.get_args(fld_type):
                    if typ is not None and val is None:
                        try:
                            val = typ(raw_val)
                        except:
                            pass
            # Simple types (?), worry about Generic?
            else:
                try:
                    val = fld_type(raw_val)
                except:
                    pass

            if val is None:
                warn(f'{row_num}: Cannot convert "{raw_val}" to "{fld_type}"')
                continue

            rec[fld_name] = val

        # Ensure all optional fields are represented
        for opt in opt_flds:
            if opt not in rec:
                rec[opt] = None

        # See if we have enough data to instantiate the class
        if len(rec) == len(fields):
            yield (cls(**rec))
