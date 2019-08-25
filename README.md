# backend-school
Яндекс. Школа бэкенд-разработки. Задание: Интернет-магазин
> Nginx + Flask + Couchbase

[![Build Status](https://travis-ci.com/xChuCx/backend-school.svg?token=eLqMXbAGhiTmx6zwgxG8&branch=master)](https://travis-ci.com/xChuCx/backend-school)

### Структура проекта:
```
.
├── docker-compose-test.yml
├── docker-compose.yml
├── backend.service
└── services
    ├── nginx
    │   ├── Dockerfile
    │   └── prod.conf
    └── citizens
        ├── Dockerfile
        ├── entrypoint.sh
        ├── gconfig.py
        ├── manage.py
        ├── project
        │   ├── __init__.py
        │   ├── api
        │   │   ├── __init__.py
        │   │   └── citizens.py
        │   ├── common
        │   │   ├── constants.py
        │   │   └── utils.py
        │   ├── config.py
        │   ├── db
        │   │   ├── Dockerfile
        │   │   ├── config.sh
        │   │   └── couchbase.py
        │   ├── schemas
        │   │   ├── __init__.py
        │   │   └── validation.py
        │   └── tests
        │       ├── __init__.py
        │       ├── base.py
        │       ├── test_config.py
        │       └── test_citizens.py
        └── requirements.txt
```
### Автотесты
Реализованы в ```tests```, сынтегрированы с GitHub через Travis CI.

### Зависимости
* Flask
* Flask-RESTful
* Flask-Testing
* gunicorn
* couchbase
* jsonschema
* numpy

### Установка
> для развертывания требуется git,docker,docker-compose
```
# Install git:
sudo apt install git

# Install docker:
sudo apt-get update
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Install docker-compose:
curl -L https://github.com/docker/compose/releases/download/1.24.1/docker-compose-`uname -s`-`uname -m` > docker-compose
chmod +x docker-compose
sudo mv docker-compose /usr/local/bin

```
```
git clone --depth=50 --branch=master https://github.com/xChuCx/backend-school.git xChuCx/backend-school
cd xChuCx/backend-school
```
### Развертывание и старт автотестов:
```
#!/bin/sh
docker-compose -f docker-compose.yml up -d --build
sleep 30
docker-compose exec citizens python manage.py test
```
### Установка и запуск службы:
```
sudo cp backend.service /etc/systemd/system/backend.service
sudo chmod 644 /etc/systemd/system/backend.service
sudo systemctl start backend
sudo systemctl enable backend
```
