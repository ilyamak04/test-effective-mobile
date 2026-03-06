Чуть отклонился от ТЗ (думаю в рамках тестового это приемлимо), прикрутил TLS с сертификатами от Let's Encrypt

# Тестовое задание Effective Mobile

Проект разворачивает простое веб-приложение на Python за `nginx` в Docker-контейнерах

https://test-efm.mcarov.ru/

## Структура проекта

```text
- backend
  - app.py
  - Dockerfile
- nginx
  - nginx.conf
- docker-compose.yaml
- README.md
```

## Как работает схема

Текущая схема запуска:

```text
host nginx + certbot
        |
        v
127.0.0.1:8081 -> docker nginx -> backend:8080
```

- `backend` — простой HTTP-сервер на Python, слушает порт `8080`
- `nginx` запущен в отдельном контейнере и проксирует запросы в `backend`
- TLS терминируется на хостовом `nginx`, потому что на хосте уже работает внешний `nginx`, обслуживающий другие сайты

## Запуск проекта

Собрать и запустить контейнеры:

```bash
docker compose up -d --build
```

Проверить состояние сервисов:

```bash
docker compose ps
```

## Проверка работы

Проверка основного маршрута:

```bash
curl http://127.0.0.1:8081/
```

Ожидаемый ответ:

```text
Hello from Effective Mobile!
```

Проверка healthcheck-маршрута:

```bash
curl http://127.0.0.1:8081/health
```

Ожидаемый ответ:

```text
ok
```

## Работа с контейнерами

Посмотреть логи всех сервисов:

```bash
docker compose logs
```

Посмотреть логи `backend`:

```bash
docker compose logs backend
```

Следить за логами в реальном времени:

```bash
docker compose logs -f
```

## Конфигурация хостового nginx

Если на сервере уже используется хостовый `nginx`, для домена `test-efm.mcarov.ru` можно добавить отдельный `server` блок и проксировать запросы в контейнерный `nginx`, который слушает только `127.0.0.1:8081`

> нужно иметь A-ДНС запись для соответсвующего домена 

Пример конфига:

```nginx
server {
    listen 80;
    server_name test-efm.mcarov.ru;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

TLS сертификат можно выпустить на хосте c помощь [certbot](https://certbot.eff.org/instructions?ws=nginx&os=pip):

```bash
sudo certbot --nginx -d test-efm.mcarov.ru
```

`certbot` сам обновит конфигурацию хостового `nginx` и включит HTTPS для домена
