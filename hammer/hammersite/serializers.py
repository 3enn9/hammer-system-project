from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    invited_users_phone_numbers = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'invite_code', 'invited_users_phone_numbers']

    def get_invited_users_phone_numbers(self, obj):
        
        invited_users = obj.invited_users.all()
        return [user.phone_number for user in invited_users]
