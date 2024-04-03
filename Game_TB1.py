import random as r

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN: str = '6891732958:AAFArylhtZlLkLEdR6IPV5vhmux6G2pDTkg'

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPTS: int = 4


users = {}


@dp.message(Command(commands=['start', 'старт']))
async def process_command_start(message):
    await message.answer("Привет. Это мой первый телеграмм бот.\n"
                         "Он предназначен для игры в 'Угадай Число', которую загадывает сам бот.\n"
                         "Создатель бота: Исаев Рамиз.\n"
                         "Что умеет бот:\n"
                         "/start - команда для включения бота.\n"
                         "/help - команда для вызова помощи.\n"
                         "/stats - команда для видимости статистики.\n"
                         "/aboutbot - команда для вызова информации о боте.\n"
                         "/rules - команда для вызова правил игры.\n\n"
                         "Напиши да, если прочёл правила и хочешь играть.")
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                        'secret_number': None,
                                        'attempts': None,
                                        'total_games': 0,
                                        'wins':0,
                                        'loses':0
                                        }
    print(users)


@dp.message(Command(commands=['stats', 'статистика', 'statistics']))
async def process_command_stats(message):
    await message.answer(f'Ваша статистика:\n'
                         f'Общие игры: {users[message.from_user.id]["total_games"]}.\n'
                         f'Количество побед: {users[message.from_user.id]["wins"]}.\n'
                         f'Количество проигрышей: {users[message.from_user.id]["loses"]}.')


@dp.message(Command(commands=['help', 'помощь']))
async def process_command_help(message):
    await message.answer("Вот ваша помощь:\n"
                         "/start - команда для включения бота, игры.\n"
                         "/help - команда для вызова помощи.\n"
                         "/stats - команда для видимости статистики.\n"
                         "/aboutbot - команда для вызова информации о боте.\n"
                         "/rules - команда для вызова правил игры.")


@dp.message(Command(commands=['aboutbot']))
async def process_command_about_game(message):
    await message.answer('Это мой первый телеграмм бот.\n'
                         'Он предназначен для игры в "Угадай Число", которую загадывает сам бот.\n'
                         'Создатель бота: Исаев Рамиз, ученик МАОУ "Лицея №27 имени А.В. Суворова". Бот был сделан в рамках проекта по информатике.')


@dp.message(Command(commands=['rules']))
async def process_command_about_game(message):
    await message.answer('Правила игры:\n'
                         '1. Бот может загадать числа от 0 до 100.\n'
                         '2. В общем у вас по 5 попыток на каждую игру.\n'
                         '3. Желаю удачи!')


@dp.message(F.text.lower().in_(['да']))
async def process_command_yes(message):
    if users[message.from_user.id]['in_game'] == True:
       await message.answer("Мы уже играем!")
    else:
        await message.answer("Начинаем играть")
        users[message.from_user.id]['secret_number'] = r.randint(0, 100)
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['attempts'] = ATTEMPTS


@dp.message(F.text.lower().in_(['нет', 'хочу закончить игру', 'завершить', 'хочу завершить игру', 'закончить']))
async def process_command_no(message):
    text = message.text.lower()
    if users[message.from_user.id]['in_game']:
        if text in ['хочу закончить игру', 'завершить', 'хочу завершить игру', 'закончить']:
            await message.answer('Игра была закончена.')
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['in_game'] = False
        elif text == 'нет':
            ...
    elif users[message.from_user.id]['in_game'] == False:
        if text in ['хочу закончить игру', 'завершить', 'хочу завершить игру', 'закончить']:
            await message.answer('Ты не в игре!')
        elif text == 'нет':
            await message.answer('Игра была отменена.')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Молодец, ты угадал(а). Игра завершилась.')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['loses'] += 1
            await message.answer('Ты потратил все попытки. Хочешь начать игру заново?')
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Нет, число меньше!')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Нет, число больше!')
    else:
        await message.answer('Ты сейчас не играешь!')


@dp.message()
async def process_command_other_messages(message):
    await message.answer('Извините, но я такого не знаю. Воспользуйтесь командой /help.')


if __name__ == '__main__':
    dp.run_polling(bot)
