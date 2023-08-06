import json

from isc_common.string import StrToBytes, BytesToStr


def BytesToJson(mybytes):
    mystring = BytesToStr(mybytes)
    _json = json.loads(mystring)
    return _json


def JsonToBytes(meyjson):
    mystring = json.dumps(meyjson)
    bytes = StrToBytes(mystring)
    return bytes
