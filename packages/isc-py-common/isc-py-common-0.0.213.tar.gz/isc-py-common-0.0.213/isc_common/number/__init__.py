from decimal import Decimal
from itertools import chain

from bitfield import BitHandler, Bit
from django.db.models import ForeignKey

from isc_common import setAttr


def DecimalToStr(value):
    if value == None:
        return ''

    try:
        # if value == 0:
        #     return None

        res = str(value)
        res.split('.')
        cel = res.split('.')[0]
        float = StrToNumber(res.split('.')[1:][0])
        if float > 0:
            return f'{cel}.{float}'
        return cel
    except IndexError:
        return value


def StrToNumber(s1):
    if s1 == None:
        return None

    if not isinstance(s1, str):
        raise Exception(f'{s1} is not str type.')

    s = s1.replace(',', '.')

    if not isinstance(s, str):
        raise Exception(f'{s} is not str type.')
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError as ex:
            return None


def IntToNumber(s):
    if s == None:
        return None

    if not isinstance(s, int):
        raise Exception(f'{s} is not int type.')

    return float(s)


def ToNumber(s):
    if s == None:
        return 0

    if isinstance(s, int):
        return IntToNumber(s)
    elif isinstance(s, str):
        return StrToNumber(s)
    elif isinstance(s, float):
        return s
    elif isinstance(s, Decimal):
        return float(s)
    else:
        raise Exception(f'{s} unknown type.')


def ToDecimal(s):
    if s == None:
        return 0

    if isinstance(s, int):
        return Decimal(s)
    elif isinstance(s, str):
        return Decimal(s)
    elif isinstance(s, float):
        return Decimal(s)
    elif isinstance(s, Decimal):
        return s
    else:
        raise Exception(f'{s} unknown type.')


def IntToDecimal(s):
    if s == None:
        return None

    if not isinstance(s, int):
        raise Exception(f'{s} is not int type.')

    return Decimal(s)


def StrToInt(s):
    if s == None:
        return None
    try:
        return int(s)
    except ValueError as ex:
        return None


def DelProps(value):
    if isinstance(value, dict):
        for key, _value in value.items():
            if isinstance(_value, BitHandler):
                setAttr(value, key, _value._value)
            elif isinstance(_value, Bit):
                setAttr(value, key, _value.is_set)
        return value
    else:
        value


def GetPropsInt(value):
    if isinstance(value, BitHandler):
        return value._value
    else:
        value


def model_2_dict(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ForeignKey):
            data[f'{f.name}_id'] = f.value_from_object(instance)
        else:
            data[f.name] = f.value_from_object(instance)
    return data


def compare_2_dict(dict1, dict2):
    if not isinstance(dict1, dict):
        raise Exception(f'dict1 must be dict')

    if not isinstance(dict2, dict):
        raise Exception(f'dict2 must be dict')

    messages = []

    for x_values, y_values in zip(dict1.items(), dict2.items()):
        if x_values != y_values:
            messages.append(f'{x_values} != {y_values}')
    return messages


class Set:
    _lst = None
    _set = None

    def __init__(self, lst):
        if isinstance(lst, set):
            self._set = set

        if isinstance(lst, list):
            self._lst = lst


    @property
    def get_set_sorted_as_original(self):
        if self._lst != None:
            return sorted(set(self._lst), key=self._lst.index)
        elif self._set != None:
            return list(self._set)
        else:
            return []


