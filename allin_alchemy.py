# Импорт необходимых компонентов из SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Настройки подключения к базе данных PostgreSQL
DB_NAME = "Test"  # Название базы данных
DB_USER = "postgres"  # Имя пользователя БД
DB_PASSWORD = "Postgres9724"  # Пароль пользователя
DB_HOST = "localhost"  # Адрес сервера БД
DB_PORT = "5432"  # Порт подключения

# Создаем базовый класс для декларативных моделей
Base = declarative_base()


# Определяем модель User, которая представляет таблицу в БД
class User(Base):
    """
    Модель пользователя, соответствует таблице 'users' в базе данных
    Содержит два поля:
    - id - первичный ключ, автоинкремент
    - name - имя пользователя (строка, не может быть NULL)
    """
    __tablename__ = 'users'  # Имя таблицы в базе данных

    # Колонка id - целое число, первичный ключ
    id = Column(Integer, primary_key=True)
    # Колонка name - строка длиной 100 символов, обязательное поле
    name = Column(String(100), nullable=False)

    def __repr__(self):
        """Строковое представление объекта User для отладки"""
        return f"<User(id={self.id}, name='{self.name}')>"


def init_db():
    """
    Инициализация подключения к базе данных и создание таблиц
    Возвращает объект сессии для работы с БД
    """
    # Создаем строку подключения в формате:
    # postgresql://user:password@host:port/database
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Создаем движок SQLAlchemy - основной интерфейс к базе данных
    engine = create_engine(DATABASE_URL)

    # Создаем все таблицы, определенные в моделях (если они еще не существуют)
    Base.metadata.create_all(engine)

    # Создаем фабрику сессий для работы с БД
    Session = sessionmaker(bind=engine)

    # Возвращаем новую сессию
    return Session()


def print_menu():
    """Выводит текстовое меню с доступными операциями"""
    print("\nВыберите операцию:")
    print("1. Создать/проверить таблицу")
    print("2. Добавить пользователя")
    print("3. Удалить пользователя")
    print("4. Показать всех пользователей")
    print("5. Найти пользователя по ID")
    print("6. Обновить имя пользователя")
    print("0. Выход")


def create_table(session):
    """
    Создает таблицу users, если она не существует
    session - объект сессии SQLAlchemy для работы с БД
    """
    try:
        # Создаем все таблицы, определенные в моделях
        Base.metadata.create_all(session.bind)
        print("✓ Таблица 'users' готова к работе")
    except SQLAlchemyError as e:
        # Обработка ошибок SQLAlchemy
        print(f"Ошибка создания таблицы: {e}")


def add_user(session):
    """
    Добавляет нового пользователя в таблицу users
    session - объект сессии SQLAlchemy
    """
    # Запрашиваем имя пользователя
    name = input("Введите имя пользователя: ").strip()
    if not name:
        print("Имя не может быть пустым!")
        return

    try:
        # Создаем новый объект User
        new_user = User(name=name)
        # Добавляем его в сессию
        session.add(new_user)
        # Фиксируем изменения в БД
        session.commit()
        print(f"✓ Пользователь '{name}' добавлен с ID {new_user.id}")
    except SQLAlchemyError as e:
        # В случае ошибки откатываем изменения
        session.rollback()
        print(f"Ошибка добавления: {e}")


def delete_user(session):
    """
    Удаляет пользователя по ID
    session - объект сессии SQLAlchemy
    """
    # Запрашиваем ID пользователя
    user_id = input("Введите ID пользователя для удаления: ").strip()
    if not user_id.isdigit():
        print("ID должен быть числом!")
        return

    try:
        # Ищем пользователя по ID
        user = session.query(User).get(int(user_id))
        if user:
            # Если пользователь найден, удаляем его
            session.delete(user)
            session.commit()
            print(f"✓ Пользователь с ID {user_id} удален")
        else:
            print(f"Пользователь с ID {user_id} не найден")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Ошибка удаления: {e}")


def list_users(session):
    """
    Выводит список всех пользователей из таблицы users
    session - объект сессии SQLAlchemy
    """
    try:
        # Получаем всех пользователей, отсортированных по ID
        users = session.query(User).order_by(User.id).all()
        if not users:
            print("В таблице нет пользователей")
            return

        # Выводим красиво отформатированную таблицу
        print("\nСписок пользователей:")
        print("+" + "-" * 23 + "+")
        print("| {:^3} | {:^15} |".format("ID", "Имя"))
        print("+" + "-" * 23 + "+")
        for user in users:
            print("| {:^3} | {:<15} |".format(user.id, user.name))
        print("+" + "-" * 23 + "+")
        print(f"Всего: {len(users)} пользователей")
    except SQLAlchemyError as e:
        print(f"Ошибка получения списка: {e}")


def find_user(session):
    """
    Находит пользователя по ID и выводит его данные
    session - объект сессии SQLAlchemy
    """
    # Запрашиваем ID пользователя
    user_id = input("Введите ID пользователя: ").strip()
    if not user_id.isdigit():
        print("ID должен быть числом!")
        return

    try:
        # Ищем пользователя по ID
        user = session.query(User).get(int(user_id))
        if user:
            # Если пользователь найден, выводим его данные
            print(f"\nНайден пользователь:")
            print("ID:", user.id)
            print("Имя:", user.name)
        else:
            print(f"Пользователь с ID {user_id} не найден")
    except SQLAlchemyError as e:
        print(f"Ошибка поиска: {e}")


def update_user(session):
    """
    Обновляет имя пользователя по ID
    session - объект сессии SQLAlchemy
    """
    # Запрашиваем ID пользователя
    user_id = input("Введите ID пользователя: ").strip()
    if not user_id.isdigit():
        print("ID должен быть числом!")
        return

    # Запрашиваем новое имя
    new_name = input("Введите новое имя: ").strip()
    if not new_name:
        print("Имя не может быть пустым!")
        return

    try:
        # Ищем пользователя по ID
        user = session.query(User).get(int(user_id))
        if user:
            # Сохраняем старое имя для сообщения
            old_name = user.name
            # Обновляем имя
            user.name = new_name
            # Фиксируем изменения
            session.commit()
            print(f"✓ Имя пользователя с ID {user_id} изменено с '{old_name}' на '{new_name}'")
        else:
            print(f"Пользователь с ID {user_id} не найден")
    except SQLAlchemyError as e:
        # В случае ошибки откатываем изменения
        session.rollback()
        print(f"Ошибка обновления: {e}")


def main():
    """
    Главная функция программы
    Управляет основным циклом работы приложения
    """
    session = None
    try:
        # Инициализируем подключение к БД
        session = init_db()
        print("✓ Подключение к PostgreSQL установлено")

        # Основной цикл программы
        while True:
            # Выводим меню
            print_menu()
            # Запрашиваем выбор пользователя
            choice = input("Ваш выбор (0-6): ").strip()

            # Обрабатываем выбор пользователя
            if choice == "0":
                break  # Выход из программы
            elif choice == "1":
                create_table(session)
            elif choice == "2":
                add_user(session)
            elif choice == "3":
                delete_user(session)
            elif choice == "4":
                list_users(session)
            elif choice == "5":
                find_user(session)
            elif choice == "6":
                update_user(session)
            else:
                print("Неверный выбор, попробуйте снова")
    except Exception as e:
        # Обработка любых неожиданных ошибок
        print(f"Критическая ошибка: {e}")
    finally:
        # В любом случае закрываем сессию
        if session:
            session.close()
            print("✓ Соединение с базой данных закрыто")


# Стандартная проверка для запуска программы
if __name__ == "__main__":
    main()