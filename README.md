# Продуктовый помощник
### Описание
Проект **Продуктовый помощник** - это галерея рецептов, с картинками и тегами. Пользователи могут создать свой рецепт, выбрав нужные ингредиенты.
### Технологии
Бэкенд написан на Python 3.8, использует Django 3.2 и Django REST Framework 3.12. Фронтенд использует React. В качестве базы данных используется PostgreSQL, веб-сервер - Nginx. Все сервисы собираются в docker-контейнерах.
### Запуск проекта в Docker-контейнерах
- Установите [Docker](https://www.docker.com/get-started) и [Docker Compose](https://docs.docker.com/compose/install/)
- Клонируйте репозиторий:
```bash
git clone https://github.com/roman-rykov/foodgram-project-react
```
- Перейдите в папку с проектом:
```bash
cd foodgram-project-react/
```
- Переименуйте `dotenv.example` в `.env`:
```bash
mv dotenv.example .env
```
- Добавьте значения ключей `DJANGO_SECRET_KEY` и `POSTGRES_PASSWORD` в файле `.env`
- Перейдите в папку `infra`, соберите и запустите контейнеры:
```bash
cd infra/
docker-compose up -d
```
- Выполните миграции, заполните базу тестовыми данными и создайте суперпользователя:
```bash
# Выполнение миграций
docker-compose exec backend python manage.py migrate
# Перенос статических файлов
docker-compose exec backend python manage.py collectstatic --noinput 
# Заполнение базы данных
docker-compose exec backend python manage.py loaddata ingredients.json tags.json
docker-compose exec backend python manage.py filldb
# Создание суперпользователя
docker-compose exec backend python manage.py createsuperuser
```
- Проект станет доступен по локальному адресу http://127.0.0.1/
### Тестовая веб-версия
Проверить работу сервиса вы можете на http://foodhelper.tk/  
Панель администратора доступна на http://foodhelper.tk/admin/  
Логин `testuser@example.org`  
Пароль `testpassword`
