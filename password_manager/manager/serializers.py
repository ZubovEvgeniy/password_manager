from rest_framework import serializers
from .models import Password
from .utils import decrypt_password
from password_manager.settings import ENCRYPT_KEY


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ('service_name', 'password')

    def to_representation(self, instance):
        """Расшифровывает пароль при получении данных."""
        data = super().to_representation(instance)
        data['password'] = decrypt_password(instance.password, ENCRYPT_KEY)
        return data
