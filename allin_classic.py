import psycopg2
from psycopg2 import sql

# Настройки подключения
DB_NAME = "Test"
DB_USER = "postgres"
DB_PASSWORD = "Postgres9724"
DB_HOST = "localhost"
DB_PORT = "5432"


def get_connection():
    """Устанавливает соединение с базой данных"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def print_menu():
    """Выводит меню операций"""
    print("\nВыберите операцию:")
    print("1. Создать/проверить таблицу users")
    print("2. Добавить пользователя")
    print("3. Удалить пользователя")
    print("4. Показать всех пользователей")
    print("5. Найти пользователя по ID")
    print("6. Обновить имя пользователя")
    print("0. Выход")


def create_table(conn):
    """1. Создает таблицу users если она не существует"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                );
            """)
            conn.commit()
            print("✓ Таблица 'users' готова к работе")
    except psycopg2.Error as e:
        print(f"Ошибка создания таблицы: {e}")
        conn.rollback()


def add_user(conn):
    """2. Добавляет нового пользователя"""
    name = input("Введите имя пользователя: ").strip()
    if not name:
        print("Имя не может быть пустым!")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name) VALUES (%s) RETURNING id;",
                (name,)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            print(f"✓ Пользователь '{name}' добавлен с ID {user_id}")
    except psycopg2.Error as e:
        print(f"Ошибка добавления: {e}")
        conn.rollback()


def delete_user(conn):
    """3. Удаляет пользователя по ID"""
    user_id = input("Введите ID пользователя для удаления: ").strip()
    if not user_id.isdigit():
        print("ID должен быть числом!")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s RETURNING id;",
                (int(user_id),)
            )
            result = cursor.fetchone()
            conn.commit()

            if result:
                print(f"✓ Пользователь с ID {user_id} удален")
            else:
                print(f"Пользователь с ID {user_id} не найден")
    except psycopg2.Error as e:
        print(f"Ошибка удаления: {e}")
        conn.rollback()


def list_users(conn):
    """4. Выводит список всех пользователей"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM users ORDER BY id;")
            users = cursor.fetchall()

            if not users:
                print("В таблице нет пользователей")
                return

            print("\nСписок пользователей:")
            print("+" + "-" * 23 + "+")
            print("| {:^3} | {:^15} |".format("ID", "Имя"))
            print("+" + "-" * 23 + "+")

            for user in users:
                print("| {:^3} | {:<15} |".format(user[0], user[1]))

            print("+" + "-" * 23 + "+")
            print(f"Всего: {len(users)} пользователей")
    except psycopg2.Error as e:
        print(f"Ошибка получения списка: {e}")


def find_user(conn):
    """5. Находит пользователя по ID"""
    user_id = input("Введите ID пользователя: ").strip()
    if not user_id.isdigit():
        print("ID должен быть числом!")
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name FROM users WHERE id = %s;",
                (int(user_id),)
            )
            user = cursor.fetchone()

            if user:
                print(f"\nНайден пользователь:")
                print("ID:", user[0])
                print("Имя:", user[1])
            else:
                print(f"Пользователь с ID {user_id} не найден")
    except psycopg2.Error as e:
        print(f"Ошибка поиска: {e}")


def update_user(conn):
    """6. Обновляет имя пользователя"""
    user_id = input("Введите ID пользователя: ").strip()
    if not user_id.isdigit():
        print("ID должен быть числом!")
        return

    new_name = input("Введите новое имя: ").strip()
    if not new_name:
        print("Имя не может быть пустым!")
        return

    try:
        with conn.cursor() as cursor:
            # Сначала проверим существование пользователя
            cursor.execute(
                "SELECT name FROM users WHERE id = %s FOR UPDATE;",
                (int(user_id),)
            )
            result = cursor.fetchone()

            if not result:
                print(f"Пользователь с ID {user_id} не найден")
                return

            old_name = result[0]
            cursor.execute(
                "UPDATE users SET name = %s WHERE id = %s;",
                (new_name, int(user_id)))
            conn.commit()
            print(f"✓ Имя пользователя с ID {user_id} изменено с '{old_name}' на '{new_name}'")
    except psycopg2.Error as e:
        print(f"Ошибка обновления: {e}")
        conn.rollback()


def main():
    """Главная функция"""
    conn = None
    try:
        conn = get_connection()
        print("✓ Подключение к PostgreSQL установлено")

        while True:
            print_menu()
            choice = input("Ваш выбор (0-6): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                create_table(conn)
            elif choice == "2":
                add_user(conn)
            elif choice == "3":
                delete_user(conn)
            elif choice == "4":
                list_users(conn)
            elif choice == "5":
                find_user(conn)
            elif choice == "6":
                update_user(conn)
            else:
                print("Неверный выбор, попробуйте снова")
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    finally:
        if conn:
            conn.close()
            print("✓ Соединение с базой данных закрыто")


if __name__ == "__main__":
    main()