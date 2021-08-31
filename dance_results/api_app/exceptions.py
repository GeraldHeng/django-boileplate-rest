# exceptions.py
from rest_framework.exceptions import APIException


class DefaultError(APIException):
    status_code = 400
    default_detail = "Something is wrong with the data"
    default_code = "something_is_wrong"
