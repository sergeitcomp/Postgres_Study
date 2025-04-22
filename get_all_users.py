# Импорт необходимых модулей
import psycopg2  # Основной драйвер для работы с PostgreSQL
from psycopg2 import sql  # Для безопасного формирования SQL-запросов

# Конфигурация подключения к базе данных (ЗАМЕНИТЕ ЭТИ ЗНАЧЕНИЯ НА СВОИ!)
DB_NAME = ""  # Имя вашей БД
DB_USER = "postgres"       # Пользователь (обычно postgres)
DB_PASSWORD = ""  # Пароль, который вы задали при установке
DB_HOST = "localhost"      # Хост (обычно localhost)
DB_PORT = "5432"           # Порт (обычно 5432)



def fetch_all_users(conn, table_name):
    """
    Получает все записи из указанной таблицы
    conn - активное подключение к базе данных
    table_name - имя таблицы для запроса
    Возвращает список кортежей в формате [(id, name), ...]
    """
    # Создаем курсор - инструмент для выполнения запросов
    with conn.cursor() as cursor:
        # Безопасно формируем SQL-запрос:
        # 1. sql.SQL() - обертка для SQL-кода
        # 2. {} - место для подстановки имени таблицы
        # 3. sql.Identifier() - защита от SQL-инъекций
        cursor.execute(
            sql.SQL("SELECT id, name FROM {};")
            .format(sql.Identifier(table_name)))

        # Получаем все строки результата
        # fetchall() возвращает список кортежей, например:
        # [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')]
        return cursor.fetchall()


def main():
    # Инициализация переменной подключения
    conn = None

    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            dbname=DB_NAME,  # Имя БД
            user=DB_USER,  # Логин
            password=DB_PASSWORD,  # Пароль
            host=DB_HOST,  # Адрес сервера
            port=DB_PORT  # Порт
        )
        print("✓ Подключение к PostgreSQL успешно установлено!")

        # Запрашиваем имя таблицы у пользователя
        table_name = input("Введите имя таблицы: ").strip()

        # Получаем данные из таблицы
        users = fetch_all_users(conn, table_name)

        # Выводим результаты
        if not users:  # Если список пуст
            print(f"\nТаблица '{table_name}' не содержит записей.")
        else:
            # Форматируем вывод как таблицу
            print("\nСписок пользователей:")
            print("+" + "-" * 23 + "+")
            print("| {:^3} | {:^15} |".format("ID", "Имя"))  # Заголовки
            print("+" + "-" * 23 + "+")

            # Выводим каждую запись
            for user in users:
                print("| {:^3} | {:<15} |".format(user[0], user[1]))

            print("+" + "-" * 23 + "+")
            print(f"Всего записей: {len(users)}")

    except psycopg2.OperationalError as e:
        # Ошибки подключения (неверный пароль, сервер не доступен)
        print(f"× Ошибка подключения: {e}")
        print("Проверьте:")
        print("- Запущен ли сервер PostgreSQL")
        print("- Правильность логина/пароля")
        print("- Название базы данных")

    except psycopg2.Error as e:
        # Другие ошибки PostgreSQL (например, таблица не существует)
        print(f"× Ошибка в запросе: {e}")

    except Exception as e:
        # Непредвиденные ошибки
        print(f"× Неизвестная ошибка: {e}")

    finally:
        # Всегда закрываем подключение, даже если была ошибка
        if conn:
            conn.close()
            print("\n✓ Соединение с базой данных закрыто")


# Стандартная проверка для запуска из командной строки
if __name__ == "__main__":
    main()