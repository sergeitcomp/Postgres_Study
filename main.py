import psycopg2
from psycopg2 import sql

# Настройки подключения (замените на свои)
DB_NAME = ""  # Имя вашей БД
DB_USER = "postgres"       # Пользователь (обычно postgres)
DB_PASSWORD = ""  # Пароль, который вы задали при установке
DB_HOST = "localhost"      # Хост (обычно localhost)
DB_PORT = "5432"           # Порт (обычно 5432)

def create_table_if_not_exists(conn, table_name):
    """Создает таблицу, если её нет."""
    with conn.cursor() as cursor:
        cursor.execute(
            sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
            """).format(sql.Identifier(table_name)))
        conn.commit()
        print(f"Таблица '{table_name}' готова!")

def insert_name(conn, table_name, name):
    """Добавляет имя в таблицу."""
    with conn.cursor() as cursor:
        cursor.execute(
            sql.SQL("INSERT INTO {} (name) VALUES (%s) RETURNING id;")
            .format(sql.Identifier(table_name)),
            (name,)
        )
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Добавлено имя '{name}' с ID = {inserted_id}")

def main():
    # Подключение к БД
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Успешное подключение к PostgreSQL!")

        # Ввод имени таблицы с клавиатуры
        table_name = input("Введите имя таблицы: ").strip()
        create_table_if_not_exists(conn, table_name)

        # Ввод имени для добавления
        while True:
            name = input("Введите имя (или 'exit' для выхода): ").strip()
            if name.lower() == 'exit':
                break
            insert_name(conn, table_name, name)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if conn:
            conn.close()
            print("Соединение закрыто.")

if __name__ == "__main__":
    main()
