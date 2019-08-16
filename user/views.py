from datetime import timedelta
from user.serializers import UserSerializer
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from common.serializers import OnlineUserTrackingSerializer


class UserRegister(ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        request_user = request.user
        user_serializer = UserSerializer(request_user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=serializer.instance)
            return_serializer = UserSerializer(user)

            view_format = {
                'status_code': status.HTTP_201_CREATED,
                'data': {
                    'user': return_serializer.data,
                    'token': token.key
                }
            }
            return Response(view_format, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Check if users are online
class UserOnline(generics.ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        user_activity_objects = OnlineUserTrackingSerializer.get_user_online_users(timedelta(minutes=10))
        return Response({
            'online_users': user_activity_objects.data,
            'message': 'Online Users List'
        }, status=status.HTTP_200_OK)
