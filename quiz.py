from Server.Core import QuizDB, QuizUserDB, DB
import asyncio

from Server.Models import Quiz


async def update_users():
    #for n in range(1, 13):
    #    question = await QuizDB.select(n)
    #    print(question)
    #question = await QuizDB.select(11)
    #print(question)

    #question = await QuizDB.select(11)
    #print(question)
    #question = await QuizDB.select(12)
    #print(question)

    #question1 = question
    #question1.id = 11

    #question.question = "Какой космический зонд первым сфотографировал обратную сторону Луны?"
    #question.variants = ['11', '19', '15', '17']
    #question.answer = '19'  # Индекс правильного ответа
    #question.desc = '''11 сентября 2024 года:  12 на МКС, 3 на «Тяньгун», 4 на Crew Dragon.'''
    #await QuizDB.update(question)
    #question = await QuizDB.select(11)
    #print(question)

    #id1 = 0
    #ids = []
    #users1 = await DB.get_all_users()
    #    if user.action.startswith('event'):
    #        user.action = 'start_menu'
    #        id1 = user.ID
    #        print(id1)
    #        await DB.update_user(user)
    #        print(user)
    #обновляем инфу об участнике квиза
    #user = await QuizUserDB.select(1289)
    #print(user)
    #user.count_true_answers = 12
    #await QuizUserDB.update(user)
    #user = await QuizUserDB.select(1289)
    #print(user)
    q = await QuizDB.select(1)
    print(q)
    #список участников

    #timer1 = users[1].end_datetime - users[1].start_datetime

    #timer2 = users[1].end_datetime - users[1].start_datetime
    #user_id1 = users[1].user_id
    #user_id2 = users[1].user_id

    #print(len(users))

    #        timer = user.end_datetime - user.start_datetime
    #        if timer < timer1:
    #            timer1 = user.end_datetime - user.start_datetime
    #            user_id1 = user.user_id
    #        elif timer < timer2:
    #            timer1 = user.end_datetime - user.start_datetime
    #            user_id1 = user.user_id
    #print(user_id1, timer1)
    #print(user_id2, timer2)


    #    if user.ID in ids:
    #        print(user.ID, user.VkFirstName, user.VkLastName)
    #for user in users:
    #    #if user.user_id == id1:

    # КАК ПОЛУЧИТЬ СПИСОК УЧАСТНИКОВ КВИЗА
    users = await QuizUserDB.get_all_users()
    quiz_users = []
    for user in users:
        if user.end_datetime:
            # print(user)
            # print(user.end_datetime - user.start_datetime)
            quiz_users.append(user)

    users1 = await DB.get_all_users()
    for user in users1:
        for i in range(len(quiz_users)):
            if user.ID == quiz_users[i].user_id:
                print(user.VkFirstName, user.VkLastName, quiz_users[i].user_id, quiz_users[i].end_datetime - quiz_users[i].start_datetime, quiz_users[i].count_true_answers)
            #print(user.VkFirstName, user)



# Запуск асинхронной функции
asyncio.run(update_users())
#839 447