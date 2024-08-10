# Калькулятор себестоимости и маржинальности товара

Обычно я делаю проект красивее. Например
 - apps отдельно будут. 
 - структурирование в application (directories, files: services, utils...)
 - .env ...


### ! Импортировать из таблицы не было в задаче

## Функциональность

- Расчет себестоимости товара
- Учет логистических расходов
- Выбор налоговой ставки
- Расчет цены продажи на основе желаемой маржи
- Расчет комиссий маркетплейса (FBS и FBO)
- Расчет стоимости доставки до клиента

## Технологии

- Python 3.11
- Django 5
- Django REST Framework 3.15.0
- PostgreSQL

## Установка

1. Клонируйте репозиторий:
   ```
   git clone _link_
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Unix или MacOS
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Настройте базу данных PostgreSQL (убедитесь, что PostgreSQL установлен):
   ```
   createdb your_database_name
   ```

5. Обновите настройки базы данных в `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. Примените миграции:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Создайте суперпользователя:
   ```
   python manage.py createsuperuser
   ```

8. Запустите сервер разработки:
   ```
   python manage.py runserver
   ```

## Использование API

Отправьте POST-запрос на эндпоинт `/api/calculate-cost/` со следующими данными:

```json
{
  "name": "Название товара",
  "purchase_price": 100.00,
  "logistics_cost": 500.00,
  "logistics_quantity": 100,
  "tax_rate": 1,
  "desired_price": 150.00,
  "margin_percentage": 20,
  "category": 1,
  "height": 10,
  "length": 20,
  "width": 15
}
```
