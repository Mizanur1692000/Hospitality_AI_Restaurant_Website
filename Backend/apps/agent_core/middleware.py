import re
from django.http import HttpResponseBadRequest
from django.conf import settings


class NgrokHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ngrok_patterns = [
            r'.*\.ngrok-free\.app$',
            r'.*\.ngrok\.io$',
            r'.*\.ngrok\.app$',
        ]

    def __call__(self, request):
        host = request.get_host().split(':')[0]

        if host in ['localhost', '127.0.0.1']:
            return self.get_response(request)

        for pattern in self.ngrok_patterns:
            if re.match(pattern, host):
                if host not in settings.ALLOWED_HOSTS:
                    settings.ALLOWED_HOSTS.append(host)
                return self.get_response(request)

        if host in settings.ALLOWED_HOSTS or '*' in settings.ALLOWED_HOSTS:
            return self.get_response(request)

        return HttpResponseBadRequest(f"Invalid host: {host}")
