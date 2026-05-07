import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication, exceptions

from service.constants import ResponseMessages
from service.models import UserActiveToken, Users


class Authentication(authentication.BaseAuthentication):
    @classmethod
    def authenticate(cls, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                if len(parts) == 1:
                    token = parts[0]
                else:
                    return None
            else:
                token = parts[1]
            try:
                payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            except jwt.ExpiredSignatureError as e:
                raise exceptions.AuthenticationFailed(f"{ResponseMessages.UNAUTHORIZED}: {e}")
            except jwt.InvalidTokenError as e:
                raise exceptions.AuthenticationFailed(f"{ResponseMessages.UNAUTHORIZED}: {e}")

            user_id = payload.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed(ResponseMessages.UNAUTHORIZED)
            user_token = UserActiveToken.objects.filter(
                user_id=user_id,
                token=token,
                is_active=True,
                expire_at__gt=timezone.now()
            ).first()
            if not user_token:
                raise exceptions.AuthenticationFailed(ResponseMessages.UNAUTHORIZED)
            user = Users.objects.filter(id=user_id, is_active=True).first()
            if not user:
                raise exceptions.AuthenticationFailed(ResponseMessages.UNAUTHORIZED)
            return (user, token)

        except exceptions.AuthenticationFailed as e:
            raise e
        except Exception as error:
            raise exceptions.AuthenticationFailed(error)
