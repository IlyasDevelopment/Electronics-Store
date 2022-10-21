Запуск сервиса:

docker-compose up --build -d

Генерация и применение миграций:

docker exec -it store_app bash

alembic revision --autogenerate -m "First Migration" && alembic upgrade head
