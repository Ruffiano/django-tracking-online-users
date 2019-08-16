from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import OnlineUsersTrackingModel
from user.models import User


class SubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OnlineUserTrackingSerializer(serializers.ModelSerializer):
    user_set = SerializerMethodField()

    class Meta:
        model = OnlineUsersTrackingModel
        fields = ['user', 'last_active_time', 'user_set']

    def get_user_set(self, obj):
        cart = User.objects.filter(id=obj.id)
        serialized = SubUserSerializer(cart, many=True)
        return serialized.data

    @staticmethod
    def update_user_online_time(user):
        OnlineUsersTrackingModel.objects.update_or_create(user_id=user, defaults={'last_active_time': timezone.now()})

    @staticmethod
    def get_user_online_users(time_delta=timedelta(minutes=15)):
        starting_time = timezone.now() - time_delta
        user = OnlineUsersTrackingModel.objects.filter(last_active_time__gte=starting_time).order_by(
            '-last_active_time')
        serializer = OnlineUserTrackingSerializer(user, many=True)
        return serializer
