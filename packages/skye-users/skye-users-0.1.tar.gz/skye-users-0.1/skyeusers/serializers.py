from rest_framework import serializers

from skyeusers.models import UserAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'first_name', 'last_name', 'role', 'photo']


class RoleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    view_skyeusers = serializers.BooleanField()
    add_skyeusers = serializers.BooleanField()
    change_skyeusers = serializers.BooleanField()
    delete_skyeusers = serializers.BooleanField()
