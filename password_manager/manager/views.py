from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Password
from .serializers import PasswordSerializer
from .utils import encrypt_password
from password_manager.settings import ENCRYPT_KEY


class PasswordView(APIView):
    """
    Представление для обработки запросов к менеджеру паролей. Поддерживает
    методы GET и POST для получения, создания и обновления паролей.
    """
    def get(self, request, service_name=None):
        """
        Обрабатывает GET-запросы.
        Args:
            request: Объект запроса.
            service_name (str, optional): Имя сервиса (если указано в URL).
        """
        if service_name:
            # Если service_name указан в URL, получаем пароль по имени сервиса
            try:
                password = Password.objects.get(service_name=service_name)
                serializer = PasswordSerializer(password)
                return Response(serializer.data)
            except Password.DoesNotExist:
                return Response({"error": "Password not found"},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            # Если service_name не указан, отдать список всех паролей
            queryset = Password.objects.all()
            search_param = request.query_params.get('service_name')
            if search_param:
                # Если параметр указан, фильтруем по совпадению имени сервиса
                queryset = queryset.filter(
                    service_name__icontains=search_param)

            serializer = PasswordSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request, service_name):
        """
        Обрабатывает POST-запросы для создания или обновления пароля.

        Args:
            request: Объект запроса.
            service_name (str): Имя сервиса (из URL).
        """
        password = request.data.get('password')
        # Зашифровываем пароль
        encrypted_password = encrypt_password(password, ENCRYPT_KEY)
        # Используем update_or_create для создания/обновления пароля в бд
        instance, created = Password.objects.update_or_create(
            service_name=service_name,
            defaults={'password': encrypted_password},
        )
        return Response(
            {'password': password},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
