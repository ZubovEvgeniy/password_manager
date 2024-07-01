from django.test import TestCase, Client
from rest_framework import status

from manager.models import Password
from manager.utils import decrypt_password, encrypt_password
from password_manager.settings import ENCRYPT_KEY


class PasswordViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """тестовый экземпляр класса Password"""

        super().setUpClass()
        cls.service_name = 'test_name'
        cls.password = 'test_password'
        Password.objects.create(
            service_name=cls.service_name,
            password=encrypt_password(cls.password, ENCRYPT_KEY))

    def setUp(self):
        self.guest_client = Client()

    def test_get_existing_password(self):
        """Тестируем получение существующего пароля."""

        response = self.guest_client.get(f'/password/{self.service_name}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Сравниваем расшифрованный пароль с тестовым
        self.assertEqual(response.data['password'], self.password)
        self.assertEqual(response.data['service_name'], self.service_name)

    def test_get_nonexistent_password(self):
        """Тестируем получение несуществующего пароля."""

        response = self.guest_client.get('/password/nonexistentservice/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_password_list(self):
        """Тестируем получение списка паролей."""

        response = self.guest_client.get('/password/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что список не пустой
        self.assertTrue(len(response.data) > 0)

    def test_create_new_password(self):
        """Тестируем создание новой пары сервис-пароль."""

        new_service_name = 'newservice'
        new_password = 'newpassword456'
        response = self.guest_client.post(
            f'/password/{new_service_name}/',
            {'password': new_password}
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что пароль вернулся в ответе
        self.assertEqual(response.data['password'], new_password)
        # Проверяем, что пароль сохранен в базе данных в зашифрованном виде
        created_password = Password.objects.get(service_name=new_service_name)
        # Сравниваем расшифрованный из БД пароль с нашим новым тестовым
        self.assertEqual(
            decrypt_password(created_password.password, ENCRYPT_KEY),
            new_password
            )

    def test_update_existing_password(self):
        """Тестируем обновление существующего пароля."""

        updated_password = 'updatedpassword789'
        response = self.guest_client.post(
            f'/password/{self.service_name}/',
            {'password': updated_password}
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что пароль вернулся в ответе
        self.assertEqual(response.data['password'], updated_password)
        # Проверяем, что пароль обновлен в базе данных в зашифрованном виде
        updated_password_entry = Password.objects.get(
            service_name=self.service_name)
        # Сравниваем расшифрованный из БД пароль с нашим обновленным тестовым
        self.assertEqual(
            decrypt_password(updated_password_entry.password, ENCRYPT_KEY),
            updated_password
            )
