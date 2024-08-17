import jwt
from django.contrib.auth import login

from restbas.models import User


import logging


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info('JWTAuthenticationMiddleware: Starting')
        token = request.COOKIES.get('jwt')
        if token:
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user_id = payload['id']
                user = User.objects.get(id=user_id)
                logging.info(
                    f'JWTAuthenticationMiddleware: User found: {user.email}'
                )
                login(request, user)
                logging.info(
                    'JWTAuthenticationMiddleware: User logged in successfully'
                )
            except jwt.ExpiredSignatureError:
                logging.info('JWTAuthenticationMiddleware: Token has expired')
                response = self.get_response(request)
                response.delete_cookie('jwt')
                return response
            except jwt.InvalidTokenError:
                logging.info('JWTAuthenticationMiddleware: Token is invalid')
                response = self.get_response(request)
                response.delete_cookie('jwt')
                return response
        logging.info('JWTAuthenticationMiddleware: Finished')
        return self.get_response(request)
