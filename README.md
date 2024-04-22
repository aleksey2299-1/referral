# Реферальная система.

[Посмотреть проект можно по ссылке](https://referral.sytes.net/)

## Оглавление <a id="contents"></a>

1. [О проекте](#about)
2. [Стек технологий](#tools)
3. [Функционал](#functional)
4. [Установка зависимостей](#installation)
5. [Запуск](#start)

## О проекте <a id="about"></a>

Простая реферальная система, разработанная в рамках тестового задания.

## Стек технологий <a id="tools"></a>

[![Typescript](https://img.shields.io/badge/TypeScript-%23404d59.svg?style=for-the-badge&logo=typescript&logoColor=blue)](https://www.typescriptlang.org/)
[![Redux](https://img.shields.io/badge/Redux-%23404d59.svg?style=for-the-badge&logo=Redux&logoColor=violet)](https://redux.js.org/)
[![React](https://img.shields.io/badge/react-%23404d59.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)](https://react.dev/)
[![HTML5](https://img.shields.io/badge/html5-%23404d59.svg?style=for-the-badge&logo=html5&logoColor=orange)](https://html.spec.whatwg.org/multipage/)
[![AntDesign](https://img.shields.io/badge/AntDesign-%23404d59.svg?style=for-the-badge&logo=antdesign&logoColor=0170FE)](https://ant.design/)
[![React Hook Form](https://img.shields.io/badge/react%20hook%20form-%23404d59.svg?style=for-the-badge&logo=reacthookform&logoColor=EC5990)](https://react-hook-form.com/)

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%204.2-blue?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-%203.14.0-blue?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2016-blue?style=for-the-badge&logo=PostgreSQL)]([https://www.postgresql.org/])
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.1.0-blue?style=for-the-badge&logo=gunicorn)](https://gunicorn.org/)
[![drf-spectacular](https://img.shields.io/badge/drf--spectacular-0.27.0-blue?style=for-the-badge)](https://drf-spectacular.readthedocs.io/)

[![Docker](https://img.shields.io/badge/Docker-white?style=for-the-badge&logo=docker&logoColor=White)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-34567C?style=for-the-badge&logo=docsdotrs&logoColor=White)](https://docs.docker.com/compose/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Certbot](https://img.shields.io/badge/certbot-003A70?style=for-the-badge&logo=letsencrypt&logoColor=white)](https://certbot.eff.org/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/ru)

## Функционал<a id="functional"></a>

Реализована простая реферальная система и имитация получения 4-х значного кода подтверждения при входе.

Репозиторий включает в себя два файла **docker-compose.yml** и 
**docker-compose.production.yml**, что позволяет развернуть проект на
локальном или удалённом серверах.

Реализовано получение и автопродление сертификатов для сайта внутри docker контейнера nginx.

## Установка зависимостей для полного разворачивания проекта<a id="installation"></a>

1. Создайте и перейдите в директорию проекта:

```bash
mkdir referrals
cd referrals/
```

2. Скачайте и добавьте файл **[docker-compose.production.yml](https://github.com/aleksey2299-1/referral/blob/main/docker-compose.production.yml)** в директорию.

3. Cоздайте файл **.env**:

```bash
nano .env
```

Добавьте следующие строки и подставьте свои значения:
````dotenv
# postgres
POSTGRES_DB=DB                           # название db
POSTGRES_USER=USER                       # имя пользователя для db
POSTGRES_PASSWORD=PASSWORD               # пароль пользователя для db
DB_HOST=db                               # если поменять, то тогда нужно поменять название сервиса в docker-compose.production.yml
DB_PORT=5432                             # это порт для доступа к db

# django
SECRET_KEY=SECRET_KEY                    # SECRET_KEY в настройках django
DEBUG=False                              # режим debug (True или False)
ALLOWED_HOSTS=127.0.0.1 backend          # ваши адреса через пробел (пример:localhost 127.0.0.1 xxxx.com)

# certbot                                # если вы не планируете его использовать, то эти переменные можно не указывать
GET_CERTS=False                          # True для получения сертификатов (обязательно укажите email в CERTBOT_EMAIL)
CERTBOT_EMAIL=example@example.com        # Email для регистрации certbot
DOMAIN=exemple.com                       # Домен на котором вы разворачиваете
````

4. [Установить docker](https://www.docker.com/get-started/)

В терминале linux это можно сделать так:

```bash
  sudo apt update
  sudo apt install curl
  curl -fSL https://get.docker.com -o get-docker.sh
  sudo sh ./get-docker.sh
  sudo apt install docker-compose-plugin
```

---

## Запуск <a id="start"></a>

1. Запустите контейнеры с проектом следующей командой (используйте флаг -d для запуска в фоновом режиме):

```bash
docker compose -f docker-compose.production.yml up
```

В терминале Linux могут потребоваться права суперпользователя:

```bash
sudo docker compose -f docker-compose.production.yml up
```

2. Для доступа в [админ-зону](http://localhost:8000/admin/):

Логин: `+79999999999`

Пароль: `admin`


После запуска проект можно будет посмотреть по [ссылке](http://localhost:8000/).

Посмотреть документацию:
[Redoc](http://localhost:8000/api/docs/)

### Если вы хотите иметь возможность поменять код:

Склонируйте репозиторий:
````bash
git clone git@github.com:aleksey2299-1/referral.git
````

Перейдите в папку forms и запустите файл **docker-compose.yml**:
````bash
cd referral
docker compose up
````

> **Примечание.** Любые изменения в коде при сохранении будут немедленно отображаться при запросах к серверу
***


[Оглавление](#contents)

