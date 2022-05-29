# Проект forfar

Техническое задание здесь: https://github.com/smenateam/assignments/tree/master/backend

## Порядок запуска
1. Склонировать репозиторий проекта https://github.com/popovpp/forfar.git
2. В корневой директории репозитория установить и активировать виртуальное окружение Python: <br>
`pip3 install virtualenv` <br>
`python3 -m venv env` <br>
`source venv/bin/activate` <br>
3. Перейти в директорию проекта и установить зависимости: <br>
`cd forfar` <br>
`pip3 install -r requirements.txt` <br>
4. Из корневой директории репозитория запустить контейнеры с сервисами postgresql, redis и wkhtmltopdf: <br>
`cd ..` <br>
`docker-compose up` <br>
Сервисы доступны на localhost на портах по умолчанию: <br>
- postgresql на 5432; <br>
- redis на 6379; <br>
- wkhtmltopdf на 80 <br>/
Перед запуском необходимо убедиться, что все указанные порты свободны. <br>
5. Открыть новое окно терминала,затем перейти в корневую директорию репозитория и активировать виртуальное окружение: <br>
`source venv/bin/activate` <br>
6. Из директории проекта запустить последовательно миграции, создание суперпользователя и заполнение таблицы Printer тестовыми данными: <br>
`cd forfar`; <br>
`python manage.py migrate`; <br>
`python manage.py creatrsuperuser`; <br>
`python manage.py loaddata fixtures/data.json`;<br>
7. Запустить сервер приложения: <br>
`python manage.py runserver` <br>
8. Открыть новое окно терминала, затем перейти в корневую директорию репозитория и активировать виртуальное окружение: <br>
`source venv/bin/activate` <br>
8. Из директории проекта запустить worker of django-rq: <br>
`cd forfar`; <br>
`python manage.py rqworker default` <br>

Админка приложения доступна по адресу http://127.0.0.1:8000/admin/ <br>
Панель django-rq доступна по адресу http://127.0.0.1:8000/django-rq/ <br>
Эндпоинты приложения доступны на хосте http://127.0.0.1:8000/ <br>
