from django.apps import AppConfig


# Конфігураційний клас для додатку 'books'
class BooksConfig(AppConfig):
    # Тип поля за замовчуванням для автоматично створюваних первинних ключів (id)
    default_auto_field = 'django.db.models.BigAutoField'

    # Ім’я додатку (має відповідати імені папки додатку)
    name = 'books'
