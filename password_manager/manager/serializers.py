from rest_framework import serializers
from .models import Password
from .utils import decrypt_password
from password_manager.settings import ENCRYPT_KEY


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ('service_name', 'password')

    def validate(self, data):
        """Проверка на совпадение имени сервиса и пароля"""
        if data['service_name'] == data['password']:
            raise serializers.ValidationError(
                'Fields must be different')
        return data

    def to_representation(self, instance):
        """Расшифровывает пароль при получении данных."""
        data = super().to_representation(instance)
        data['password'] = decrypt_password(instance.password, ENCRYPT_KEY)
        return data
