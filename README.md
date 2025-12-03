furnitureStore

Проект демонстрирует работу с MySQL: создание базы данных, таблиц, индексов, вставку данных через Python и использование простого Python-агента для работы с SQL-запросами.

Структура проекта
furnitureStore/
│
├── database_init.sql       # Скрипт создания базы данных и таблиц
├── indexex.sql             # Скрипт создания индексов
├── insert-python.py        # Пример вставки данных в базу
├── python_ai_agent.py      # Агент для генерации и выполнения SQL-запросов
└── README.md

1. Инициализация базы данных

Создание базы данных и всех необходимых таблиц:

mysql -u root -p < database_init.sql


После выполнения будет создана база furniture_store и таблицы, описанные в SQL-скрипте.

2. Создание индексов

Выполнение индексов для оптимизации работы запросов:

mysql -u root -p furniture_store < indexex.sql

3. Вставка данных (Python)

Перед запуском необходимо установить библиотеку:

pip install mysql-connector-python


Обновите параметры подключения в файле insert-python.py:

config = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "furniture_store"
}


Запуск:

python insert-python.py

4. Python SQL агент (python_ai_agent.py)

Агент может генерировать SQL-запросы и выполнять их.

Установка зависимостей:

pip install langchain langchain-community langchain-core groq


Запуск:

python python_ai_agent.py

Требования

Python 3.10+

MySQL 8+

Библиотеки:

mysql-connector-python

langchain / langchain-community

groq или другой провайдер LLM

Быстрый старт

Создать базу данных:

mysql -u root -p < database_init.sql


Создать индексы:

mysql -u root -p furniture_store < indexex.sql


Вставить данные:

python insert-python.py


Запустить SQL-агента:

python python_ai_agent.py
