from http import HTTPStatus

from django.test import TestCase, Client

from manager.models import Password
from manager.utils import encrypt_password
from password_manager.settings import ENCRYPT_KEY


class ManagerURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """тестовый экземпляр класса Password"""

        super().setUpClass()
        Password.objects.create(
            service_name='test_name',
            password=encrypt_password('test_password', ENCRYPT_KEY)
        )

    def setUp(self):
        self.guest_client = Client()

    def test_url_names_exists_at_desired_location(self):
        """Страница списка пар "название сервиса - пароль"
        Страница имени сервиса
        Страница, найденная по части имени сервиса"""

        url_names = [
            '/password/',
            '/password/test_name/',
            '/password/?service_name=na',
        ]
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_names_does_not_exists_at_desired_location(self):
        """Страница /password/unknown/ не найдена"""

        response = self.guest_client.get('/password/unknown/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
