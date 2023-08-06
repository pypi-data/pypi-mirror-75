from .cfcompare import version, standardnames, descriptions, uom, aliases, compare, grib, amip, getcf, cfname, find

# if somebody does "from cfcompare import *", this is what they will
# be able to access:
__all__ = [
    'version',
    'standardnames',
    'descriptions',
    'uom',
    'aliases',
    'compare',
    'grib',
    'amip',
    'getcf',
    'cfname',
    'find',
]