from django.db import models


class Password(models.Model):
    service_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название сервиса',
        )
    password = models.CharField(
        max_length=255,
        verbose_name='Пароль сервиса',
        )

    def __str__(self):
        return self.service_name
