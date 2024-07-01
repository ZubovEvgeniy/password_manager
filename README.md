# Password manager

## Описание

Сервис хранения паролей, работающий на основе GET и POST запросов.
Пароль сохраняется в базу данных и привязывается к имени сервиса, указанный при сохранении пароля.

## Реализованные функции

 - Пароли хранятся в базе данных в зашифрованном виде
 - Проект доступен в [DockerHub](https://hub.docker.com/repository/docker/evgeniyzubov/password_manager/general)
 - Код покрыт тестами Unittest
 - Доступна админ панель http://localhost/admin/

## Запуск из образа Docker Compose
##### Шаг 1. Клонирование репозитория
Склонируйте репозиторий на локальную машину:
```bash
git clone git@github.com:ZubovEvgeniy/password_manager.git
```
##### Шаг 2. Заполнить файл переменных окружения
В корне проекта создайте файл ".env" по образцу ".env.example"

##### Шаг 3.  Запуск контейнеров
Из корня проекта запустите команду
```bash
docker-compose up -d --build 
```
##### Шаг 4.  Установка миграций, создание супер пользователя, сбор статики, запуск тестов
Последовательно запустите следующие команды:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py test
```

## API Reference

Для взаимодействия с сервисом отправьте запросы:

**POST** http://localhost/password/{service_name}/
Создать новый пароль или заменить существующий пароль
В теле запроса передать password, в url адресе указать service_name 
Запрос:
``` json
{
	"password": "very_secret_pass"
}
```
Ответ:
``` json
{
	"password": "very_secret_pass"
}
```

**GET** http://localhost/password/{service_name}/
Запросить пароль по имени сервиса
Ответ:
``` json
{
	"service_name": "{service_name}",
	"password": "very_secret_pass"
}
```

**GET** http://localhost/password/?service_name={part_of_service_name}
Запросить пароль по части имени сервиса
Ответ:
``` json
{
	"service_name": "{service_name}",
	"password": "very_secret_pass"
}
```
**GET** http://localhost/password/
Запросить список сервисов и паролей

## Технологии
* Python 3.9
* Django 4.2.13
* DRF 3.15.2
* Cryptography 42.0.8
* PostgreSQL
* Docker


**Автор**

Евгений Зубов

2024
