from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class RequestResponseLoggingMiddleware(MiddlewareMixin):    
    def process_response(self, request, response):
        print(f"URL: {request.path}")
        if response.status_code == 302 and request.path == '/admin/login/':
            return redirect('/vocabulary_test/')
        return response