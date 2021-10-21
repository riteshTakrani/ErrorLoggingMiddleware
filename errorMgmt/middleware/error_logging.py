from django.conf import settings
from django.utils import timezone
from datetime import datetime
from errorMgmt.models import *


class ErrorLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        self.cached_request_body = request.body
        response = self.get_response(request)
        # self.process_request(request, response)
        response = self.process_response(request, response)
        print(response)
        return response

    def process_response(self, request, response):
        print("this is scc : ", response.status_code)
        if response.status_code in settings.STATUS_CODES:
            time_now = datetime.now(tz=timezone.utc)
            status = response.status_code
            error = response.content
            error_data = ResponseModel(status=status, error=error, entry_date=time_now)
            error_data.save()
            response.status_code = 200
            response.content = "Error"
        return response
