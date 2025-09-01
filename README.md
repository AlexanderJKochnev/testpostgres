# README.md
Тестовая база данных Postgresql
1. строка подключения
   1. DATABASE_URL = 'postgresql+asyncpg://test_user:test@localhost:2345/test_db'

Тестовая база MongoDB
1. # Генерируем ключ длиной 600 символов (минимум 6)
mkdir mongokey
cd mongokey

openssl rand -base64 600 > mongo-keyfile
chmod 600 mongo-keyfile
2. 
