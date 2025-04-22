# Импортируем библиотеку для работы с PostgreSQL
import psycopg2
# Импортируем модуль sql для безопасного формирования SQL-запросов
from psycopg2 import sql

# Настройки подключения к базе данных (замените на свои реальные данные)
DB_NAME = ""  # Имя вашей БД
DB_USER = "postgres"       # Пользователь (обычно postgres)
DB_PASSWORD = ""  # Пароль, который вы задали при установке
DB_HOST = "localhost"      # Хост (обычно localhost)
DB_PORT = "5432"           # Порт (обычно 5432)


def get_user_by_id(conn, table_name, user_id):
    """
    Функция для получения имени пользователя по его ID
    conn - подключение к базе данных
    table_name - имя таблицы в базе данных
    user_id - ID пользователя, которого ищем
    """
    # Создаем курсор - это как "указатель" для работы с базой данных
    with conn.cursor() as cursor:
        # Формируем безопасный SQL-запрос
        # sql.Identifier защищает от SQL-инъекций при подстановке имен таблиц
        # %s - placeholder для параметров (защита от SQL-инъекций)
        cursor.execute(
            sql.SQL("SELECT name FROM {} WHERE id = %s;")
            .format(sql.Identifier(table_name)),  # Подставляем имя таблицы
            (user_id,)  # Подставляем user_id вместо первого %s
        )
        # Получаем результат запроса (первую найденную строку)
        result = cursor.fetchone()
        # Если результат есть - возвращаем имя (первый столбец), иначе None
        return result[0] if result else None


def update_user_name(conn, table_name, user_id, new_name):
    """
    Функция для обновления имени пользователя
    conn - подключение к базе данных
    table_name - имя таблицы
    user_id - ID пользователя
    new_name - новое имя для установки
    """
    with conn.cursor() as cursor:
        # Формируем UPDATE-запрос для изменения имени
        cursor.execute(
            sql.SQL("UPDATE {} SET name = %s WHERE id = %s;")
            .format(sql.Identifier(table_name)),
            (new_name, user_id)  # Подставляем параметры
        )
        # Подтверждаем изменения в базе данных
        conn.commit()
        print(f"Имя пользователя с ID {user_id} обновлено на '{new_name}'.")


def main():
    # Инициализируем переменную для подключения
    conn = None
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            dbname=DB_NAME,  # Имя базы данных
            user=DB_USER,  # Имя пользователя
            password=DB_PASSWORD,  # Пароль
            host=DB_HOST,  # Адрес сервера
            port=DB_PORT  # Порт
        )
        print("Успешное подключение к PostgreSQL!")

        # Запрашиваем у пользователя имя таблицы для работы
        table_name = input("Введите имя таблицы: ").strip()

        # Основной цикл программы
        while True:
            try:
                # Запрашиваем ID пользователя
                user_id = input("\nВведите ID пользователя (или 'exit' для выхода): ").strip()

                # Проверяем, не хочет ли пользователь выйти
                if user_id.lower() == 'exit':
                    break

                # Преобразуем введенный ID в число
                user_id = int(user_id)

                # Получаем имя пользователя по ID
                name = get_user_by_id(conn, table_name, user_id)

                # Если пользователь не найден
                if name is None:
                    print(f"Пользователь с ID {user_id} не найден.")
                    continue  # Переходим к следующей итерации цикла

                # Выводим текущее имя пользователя
                print(f"\nТекущее имя пользователя с ID {user_id}: {name}")

                # Спрашиваем, нужно ли редактировать
                choice = input("Хотите отредактировать имя? (yes/no): ").strip().lower()
                if choice == 'yes':
                    # Запрашиваем новое имя
                    new_name = input("Введите новое имя: ").strip()
                    # Обновляем имя в базе данных
                    update_user_name(conn, table_name, user_id, new_name)
                else:
                    print("Редактирование отменено.")

            except ValueError:  # Если введен не числовой ID
                print("Ошибка: ID должен быть числом!")
            except psycopg2.Error as e:  # Ошибки PostgreSQL
                print(f"Ошибка базы данных: {e}")
            except Exception as e:  # Все остальные ошибки
                print(f"Неизвестная ошибка: {e}")

    finally:
        # Этот блок выполнится в любом случае, даже если возникла ошибка
        if conn:  # Если подключение было установлено
            conn.close()  # Закрываем подключение
            print("\nСоединение с базой данных закрыто.")


# Стандартная проверка для запуска программы
if __name__ == "__main__":
    main()