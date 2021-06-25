import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from customers.models import Customer


AUTH_HEADER_PREFIX = ['Bearer', 'Token']

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None
        
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if not prefix in AUTH_HEADER_PREFIX:
            return None

        user = None
        if prefix.lower() == 'Bearer'.lower():
            user = self.deserialize_jwt(token)

        if user is None:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('This user has been deactivated.')

        return (user, token)

    def deserialize_jwt(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            raise exceptions.AuthenticationFailed('Invalid authentication. Could not decode token.')
        try:
            user = Customer.objects.get(pk=payload['id'])
        except Customer.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found.')
        return user
