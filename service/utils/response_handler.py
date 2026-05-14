from rest_framework import status
from rest_framework.response import Response


class ResponseHandler(Response):
    def __init__(
            self,
            success=True,
            message=None,
            errors=None,
            meta=None, 
            data=None, 
            status=status.HTTP_200_OK
        ):
        response_data={}
        if success:
            response_data["success"] = success
        if message:
            response_data["message"] = message
        if errors:
            response_data["errors"] = errors
        if meta:
            response_data["meta"] = meta
        if data:
            response_data["data"] = data

        super().__init__(data=response_data, status=status)
