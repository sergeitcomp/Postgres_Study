from vkbottle.bot import Bot, Message
from sqlalchemy.orm import Session
from models import Appeal, Manager, Topic, Status
from config import SessionLocal, MANAGERS, BOT_TOKEN
from typing import Optional

bot = Bot(token=BOT_TOKEN)

# Функция для работы с базой данных
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_manager_by_topic(topic: Topic, db: Session) -> Optional[Manager]:
    return db.query(Manager).filter(Manager.topic == topic).first()

@bot.on.message(text="Начать")
async def start_handler(message: Message):
    await message.answer(
        "Привет! Это бот Студсовета МГУ.\n"
        "Выбери тему обращения:\n"
        "1. Быт\n"
        "2. Стипендии\n"
        "3. Учебный процесс\n"
        "4. Спорт\n"
        "5. Международные вопросы"
    )

@bot.on.message(text=["1", "2", "3", "4", "5"])
async def topic_handler(message: Message):
    topics = {
        "1": Topic.LIFE,
        "2": Topic.SCHOLARSHIP,
        "3": Topic.STUDY,
        "4": Topic.SPORT,
        "5": Topic.INTERNATIONAL
    }

    topic = topics.get(message.text)
    if topic:
        await message.answer(f"Выбрана тема: {topic.value}\nНапиши текст обращения:")
        db = next(get_db())
        appeal = Appeal(student_id=message.from_id, topic=topic, text="", status=Status.NEW)
        db.add(appeal)
        db.commit()
        db.refresh(appeal)
        await message.answer(f"Создано обращение №{appeal.id}. Напиши текст обращения.")
    else:
        await message.answer("Пожалуйста, выбери тему из списка (1-5)")



@bot.on.message(text=lambda text: text.lower().startswith("ответ"))
async def response_handler(message: Message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            raise ValueError

        appeal_id = int(parts[1])
        response_text = parts[2]

        db = next(get_db())
        appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()

        if not appeal:
            await message.answer("Обращение с таким номером не найдено")
            return

        if appeal.status != Status.NEW:
            await message.answer("На это обращение уже был дан ответ")
            return

        appeal.status = Status.RESOLVED
        appeal.response = response_text
        db.commit()

        await bot.api.messages.send(
            user_id=appeal.student_id,
            message=f"Ответ на обращение #{appeal.id}\n"
                    f"Тема: {appeal.topic.value}\n"
                    f"Ответ: {response_text}",
            #random_id=0
        )

        await message.answer("Ответ успешно отправлен студенту")

    except Exception:
        await message.answer("Неправильный формат команды. Пример: Ответ 42 Ваше обращение рассмотрено")
#Обработка функции статус
@bot.on.message(text="Статус <appeal_id:int> <status>")
async def status_handler(message: Message, appeal_id: int, status: str):
    try:
        status_enum = Status[status.upper()]
    except KeyError:
        await message.answer("Неверный статус. Возможные: NEW, IN_PROGRESS, RESOLVED")
        return

    db = next(get_db())
    appeal = db.query(Appeal).filter(Appeal.id == appeal_id).first()

    if not appeal:
        await message.answer("Обращение с таким номером не найдено")
        return

    appeal.status = status_enum
    db.commit()

    await message.answer(f"Статус обращения #{appeal_id} изменен на {status_enum.value}")


@bot.on.message()
async def appeal_handler(message: Message):
    db = next(get_db())

    # Ищем самое новое обращение этого пользователя
    appeal = db.query(Appeal).filter(Appeal.student_id == message.from_id, Appeal.status == Status.NEW).first()

    if appeal:
        # Обновляем текст обращения
        appeal.text = message.text
        db.commit()

        # Проверяем наличие менеджера для этой темы
        manager = get_manager_by_topic(appeal.topic, db)
        if manager:
            appeal.manager_id = manager.id
            db.commit()

            try:
                # Проверяем разрешение на отправку сообщения менеджеру
                await bot.api.messages.send(
                    user_id=manager.vk_id,
                    message=f"Новое обращение #{appeal.id}\n"
                            f"Тема: {appeal.topic.value}\n"
                            f"Текст: {message.text}\n\n"
                            f"Чтобы ответить, отправь:\n"
                            f"Ответ [номер] [текст ответа]",
                    random_id=0
                )
            except Exception as e:
                # Обработка ошибок при отправке сообщения
                print(f"Ошибка при отправке сообщения менеджеру: {e}")

        await message.answer(f"Обращение #{appeal.id} принято!\nТема: {appeal.topic.value}")
    else:
        await message.answer("Вы ещё не начали писать обращение.\nВведите номер темы для начала.")

if __name__ == "__main__":
    from config import engine
    from models import Base

    Base.metadata.create_all(bind=engine)

    db = next(get_db())
    for vk_id, topic in MANAGERS.items():
        if not db.query(Manager).filter(Manager.vk_id == vk_id).first():
            manager = Manager(vk_id=vk_id, name=f"Manager {vk_id}", topic=topic)
            db.add(manager)
    db.commit()

    bot.run_forever()
