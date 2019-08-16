from rest_framework.authtoken.models import Token
from django.utils.deprecation import MiddlewareMixin
from .serializers import OnlineUserTrackingSerializer


class CheckOnlineUsersMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is not None:
            user_id = Token.objects.get(key=token.split(' ')[1]).user_id
            if user_id is None:
                return

            OnlineUserTrackingSerializer.update_user_online_time(user_id)
