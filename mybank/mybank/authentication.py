from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.utils import timezone


class SessionJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, token = result
        session_key = token.get('session_key')
        if not session_key:
            return user, token  # token issued before session tracking — pass through
        from account.models import UserSession
        session = UserSession.objects.filter(session_key=session_key, is_active=True).first()
        if not session:
            raise InvalidToken('Session has been revoked. Please login again.')
        UserSession.objects.filter(id=session.id).update(last_seen=timezone.now())
        return user, token
