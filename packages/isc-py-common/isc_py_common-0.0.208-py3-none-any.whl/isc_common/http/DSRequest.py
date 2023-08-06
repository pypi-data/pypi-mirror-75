import logging

from isc_common import setAttr, delAttr
from isc_common.http.RPCRequest import RPCRequest
from isc_common.json import BytesToJson

logger = logging.getLogger(__name__)


class RequestData:
    def __init__(self, _dict=None, request=None):
        if request:
            self.__data_dict__ = request.get_data()
        elif _dict:
            self.__data_dict__ = _dict
        else:
            self.__data_dict__ = dict()
        super()

    def getDataOfKey(self, key, default=None):
        return self.__data_dict__.get(key, default)

    def update(self, key, value):
        self.__data_dict__.update((key, value))
        return RequestData(self.__data_dict__)

    def getDataWithOutField(self, list_fields):
        if isinstance(list_fields, list):
            return RequestData({key: self.__data_dict__[key] for key in self.__data_dict__ if not key in list_fields})
        else:
            return RequestData(self.__data_dict__)

    def getDataNotContain(self, *sub_strs):
        res = RequestData()
        for sub in sub_strs:
            self.__data_dict__ = {key: self.__data_dict__[key] for key in self.__data_dict__ if not str(key).__contains__(sub)}
        return RequestData(self.__data_dict__)

    def dict(self):
        return self.__data_dict__


class DSRequest(RPCRequest):
    alive_only = None
    begdate = None
    dataPageSize = 75
    drawAheadRatio = 1.2
    enabledAll = None
    enddate = None
    endRow = None
    json = None
    startRow = None
    tag = None
    httpHeaders = None
    visibleMode = 'none'

    _user = None

    @property
    def user(self):
        from isc_common.auth.models.user import User
        if self._user == None:
            if self.httpHeaders != None and self.httpHeaders.USER_ID:
                self._user = User.objects.get(id=self.httpHeaders.USER_ID)
                return self._user
            else:
                if self.transaction != None:
                    operations = self.transaction.operations
                    if isinstance(operations, list):
                        for operation in operations:
                            data = operation.data
                            if data.httpHeaders != None and data.httpHeaders.USER_ID != None:
                                self._user = User.objects.get(id=data.httpHeaders.USER_ID)
                                return self._user

                raise Exception('user not enable type')
        return self._user

    @property
    def user_id(self):
        return self.user.id

    @property
    def fio(self):
        return self.user.get_short_name

    @property
    def username(self):
        return self.user.username

    @property
    def is_admin(self):
        return self.user.is_admin

    @property
    def is_develop(self):
        return self.user.is_develop

    def set_user_data(self, user):
        from isc_common.auth.models.user import User
        if isinstance(user, int):
            self._user = User.objects.get(id=user)
        elif isinstance(user, str):
            self._user = User.objects.get(username=user)
        else:
            raise Exception('user not enable type')

    def __init__(self, request):

        if request != None and request.body != b'':
            self.json = BytesToJson(request.body)
            if isinstance(self.json, dict) and len(self.json) > 0:
                data = self.json.get('data')
                if isinstance(data, dict):
                    httpHeaders = data.get('httpHeaders')
                    if isinstance(httpHeaders, dict):

                        if httpHeaders.get('WS_CHANNEL') != None:
                            self.ws_channel = httpHeaders.get('WS_CHANNEL')

                        if httpHeaders.get('WS_PORT') != None:
                            self.ws_port = httpHeaders.get('WS_PORT')

                        if httpHeaders.get('HOST') != None:
                            self.host = httpHeaders.get('HOST')

                        if httpHeaders.get('USERNAME') != None:
                            self.set_user_data(user=httpHeaders.get('USERNAME'))

                        if httpHeaders.get('USER_ID') != None:
                            self.set_user_data(user=httpHeaders.get('USER_ID'))

                        delAttr(self.json.get('data'), 'httpHeaders')
                    else:
                        if data.get('user_id') != None:
                            self.set_user_data(user=data.get('user_id'))
                else:
                    login = self.json.get('login')
                    if login != None:
                        self.set_user_data(user=login)
                    else:
                        httpHeaders = self.json.get('httpHeaders')
                        if httpHeaders != None:
                            self.set_user_data(user=httpHeaders.get('USER_ID'))

        RPCRequest.__init__(self, self.json)

    def get_data(self, excluded_keys=['grid']):
        res = None
        if isinstance(self.json, dict):
            data = self.json.get('data')
            if isinstance(data, dict):
                res = data
            elif isinstance(data, str):
                return data
            else:
                res = self.json

            res = dict((key, value) for (key, value) in res.items() if not key.startswith('_') and key not in excluded_keys)
        return res

    def get_all_data(self, excluded_keys=['grid']):
        res = None
        if isinstance(self.json, dict):
            data = self.json.get('data')
            if isinstance(data, dict):
                res = data
            elif isinstance(data, str):
                return data
            else:
                res = self.json

        return res

    def set_data(self, data):
        if isinstance(data, dict):
            setAttr(self.json, 'data', data)

    def set_criteria(self, criteria, excluded_keys=['grid']):
        data = self.get_all_data(excluded_keys=excluded_keys)
        if isinstance(data, dict):
            setAttr(data, 'criteria', criteria)

    def get_criteria(self, excluded_keys=['grid']):
        data = self.get_data(excluded_keys=excluded_keys)
        criteria = data.get('criteria')
        if isinstance(criteria, list):
            return criteria
        else:
            return []

    def get_data_array(self, excluded_keys=['grid']):
        res = None
        if isinstance(self.json, dict):
            transaction = self.json.get('transaction')
            if transaction:
                operations = transaction.get('operations')
            else:
                return (False, [self.get_data()])

            res = (True, [dict((key, value) for (key, value) in operation.items() if not str(key).startswith('_') and key not in excluded_keys) for operation in operations])
            # res = (True, [dict((key, value) for (key, value) in operation.items() if value is not None and not str(key).startswith('_') and key not in excluded_keys) for operation in operations])
        return res

    def get_oldValues(self, excluded_keys=['grid']):
        res = None
        if isinstance(self.json, dict):
            if self.json.get('oldValues', None) and isinstance(self.json.get('oldValues', None), dict):
                res = self.json.get('oldValues')
            else:
                res = self.json

            res = dict((key, value) for (key, value) in res.items() if not str(key).startswith('_') and key not in excluded_keys)
            # res = dict((key, value) for (key, value) in res.items() if value is not None and not str(key).startswith('_') and key not in excluded_keys)
        return res

    def get_id(self):
        return self.get_data().get('id', self.get_oldValues().get('id'))

    def get_operationtype(self):
        return self.json.get('operationType')

    def get_username(self):
        return self.get_data().get('username')

    def get_ids(self):
        multi, data_array = self.get_data_array()
        if data_array:
            if multi:
                ids = [record.get('data').get('id') for record in data_array]
            else:
                ids = [record.get('data').get('id') if record.get('data') else record.get('id') for record in data_array]
        else:
            ids = [0]
        return [id for id in ids if id is not None]

    def get_tuple_ids(self):
        multi, data_array = self.get_data_array()
        if data_array:
            if multi:
                ids = [(record.get('data').get('id'), record.get('visibleMode', 'none')) for record in data_array]
            else:
                ids = [(record.get('data').get('id'), self.visibleMode) if record.get('data') else (record.get('id'), self.visibleMode) for record in data_array]
        else:
            ids = [(0, "none")]
        return ids

    def get_old_ids(self):
        multi, data_array = self.get_data_array()
        if data_array:
            if multi:
                ids = [record.get('oldValues').get('id') for record in data_array]
            else:
                ids = [record.get('oldValues').get('id') if record.get('oldValues') else record.get('id') for record in data_array]
        else:
            ids = [0]
        return [id for id in ids if id is not None]

    def __str__(self):
        return str(self.__dict__)
