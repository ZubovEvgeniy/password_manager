from rest_framework import serializers
from .models import Password


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ('service_name', 'password')

    def validate(self, data):
        if data['service_name'] == data['password']:
            raise serializers.ValidationError(
                'Fields must be different')
        return data
