from django.test import TestCase

from manager.models import Password


class PasswordModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """тестовый экземпляр класса Password"""

        super().setUpClass()
        cls.password = Password.objects.create(
            service_name='testname',
            password='testpassword'
        )

    def test_service_name_verbose(self):
        """verbose_name в полях совпадает с ожидаемым"""

        password = PasswordModelTest.password
        field_verboses = {
            'service_name': 'Название сервиса',
            'password': 'Пароль сервиса'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    password._meta.get_field(field).verbose_name,
                    expected_value)

    def test_object_name_is_title_fild(self):
        """__str__ Password - строчка с содержимым password.service_name"""

        password = PasswordModelTest.password
        expected_object_name = password.service_name
        self.assertEqual(expected_object_name, str(password))
