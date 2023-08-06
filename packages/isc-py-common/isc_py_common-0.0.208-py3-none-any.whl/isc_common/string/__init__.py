def get_NoneStr(str):
    if str == None:
        return ''
    else:
        return str


def get_NullStr(str):
    if str == None:
        return ''
    elif str == 'null':
        return ''
    else:
        return str

def StrToBytes(mystring):
 return mystring.encode('utf-8')

def BytesToStr(mybytes):
 return mybytes.decode('utf-8')
