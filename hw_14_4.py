from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())

kb = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb.row(button1,button2)

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb_start.row(button1, button2)
kb_start.add(button3)

kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_buy.row(button1, button2, button3, button4)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        product_id, title, description, price = product
        await message.answer(f'Название: {title} | Описание | {description} | Цена | {price}')

        image_path = f'{product_id}.png'
        with open(image_path, 'rb') as img:
            await message.answer_photo(img)

    await message.answer('Выберите продукт для покупки', reply_markup=kb_buy)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_start)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight_=message.text)
    data = await state.get_data()
    amount_calories = (10 * float(data['weight_'])) + (6.25 * float(data['growth_'])) - (5 * float(data['age_']) + 5)
    await message.answer(f'Ваша норма калорий {amount_calories}')
    await state.finish()

if __name__ == '__main__':
    initiate_db()

    products = get_all_products()

    if not products:
        add_products('Апельсин', 'Апельсин вкусно и полезно', 100)
        add_products('Морковь', 'Морковь просто полезно', 50)
        add_products('Мультивитамины', 'Для альфача с Патриков', 2000)
        add_products('Клизма', 'Если ничто другое не помогает', 20)

        products = get_all_products()

    for product in products:
        print(product)

    executor.start_polling(dp, skip_updates=True)

