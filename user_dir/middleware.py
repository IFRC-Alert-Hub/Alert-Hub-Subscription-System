from django.contrib.auth.middleware import (
    AuthenticationMiddleware as DjangoAuthenticationMiddleware,
)
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import (
    MessageMiddleware as DjangoMessageMiddleware,
)
from django.contrib.sessions.middleware import (
    SessionMiddleware as DjangoSessionMiddleware,
)


class _GraphqlDisabledMiddlewareMixin:
    @staticmethod
    def is_graphql_request(request):
        return request.path_info.startswith("/graphql")

    def process_request(self, request):
        if self.is_graphql_request(request):
            return None
        try:
            return super().process_request(request)
        except AttributeError:
            return None

    def process_response(self, request, response):
        if self.is_graphql_request(request):
            return response
        try:
            return super().process_response(request, response)
        except AttributeError:
            return response


class AuthenticationMiddleware(
    _GraphqlDisabledMiddlewareMixin, DjangoAuthenticationMiddleware
):
    def process_request(self, request):
        if self.is_graphql_request(request):
            request.user = AnonymousUser()

        return super().process_request(request)


class SessionMiddleware(_GraphqlDisabledMiddlewareMixin, DjangoSessionMiddleware):
    pass


class MessageMiddleware(_GraphqlDisabledMiddlewareMixin, DjangoMessageMiddleware):
    pass
