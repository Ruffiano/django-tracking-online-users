from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    # email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

