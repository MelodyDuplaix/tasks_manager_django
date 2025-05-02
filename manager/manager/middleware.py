from django.utils.deprecation import MiddlewareMixin

class BearerTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header and not auth_header.startswith('Bearer '):
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {auth_header}'