from rest_framework.exceptions import APIException
from rest_framework import status
from .messages import ToastMessages


class NotFoundItemHttpException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ToastMessages.USER_iTEM_NOT_FOUND.value


class ItemExistHttpException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = ToastMessages.ITEM_EXISTS.value
