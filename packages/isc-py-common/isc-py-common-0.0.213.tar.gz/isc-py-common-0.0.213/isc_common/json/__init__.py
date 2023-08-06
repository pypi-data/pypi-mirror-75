import json
from json import JSONDecodeError

from isc_common.string import StrToBytes, BytesToStr


def BytesToJson(mybytes):
    try:
        mystring = BytesToStr(mybytes)
        _json = json.loads(mystring)
        return _json
    except JSONDecodeError:
        return dict()

def JsonToBytes(meyjson):
    mystring = json.dumps(meyjson)
    bytes = StrToBytes(mystring)
    return bytes
