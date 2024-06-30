from django.test import TestCase

from manager.models import Password
from manager.serializers import PasswordSerializer
from manager.utils import encrypt_password
from password_manager.settings import ENCRYPT_KEY


class PasswordSerializerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """Подготовка перед запуском всех тестов."""

        super().setUpClass()
        cls.service_name = 'test_service'
        cls.password = 'test_password'
        cls.encrypted_password = encrypt_password(cls.password, ENCRYPT_KEY)
        cls.password_obj = Password.objects.create(
            service_name=cls.service_name,
            password=cls.encrypted_password
        )

    def test_serialize_valid_data(self):
        """Проверяет сериализацию валидных данных."""

        serializer = PasswordSerializer(instance=self.password_obj)
        serialized_data = serializer.data
        self.assertEqual(serialized_data['service_name'], self.service_name)
        self.assertEqual(serialized_data['password'], self.password)

    def test_to_representation_with_encrypted_password(self):
        """Тестируем to_representation с уже зашифрованным паролем."""

        instance = Password(
            service_name=self.service_name,
            password=self.encrypted_password)
        serializer = PasswordSerializer(instance=instance)
        serialized_data = serializer.data
        self.assertEqual(serialized_data['service_name'], self.service_name)
        # Проверяем, что пароль расшифрован
        self.assertEqual(serialized_data['password'], self.password)
