from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

api = "7509441697:AAGX1eyKfIrHf5gFnXVjnxfKm1VYSkIOQFs"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Calories")
async def set_age(message):
    await message.answer("Введите свой возраст (в годах):")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f'Если Вы мужчина, то Ваша норма колорий: '
                         f'{10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5}')
    await message.answer(f'Если Вы женщина, то Ваша норма колорий: '
                         f'{10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161}')

    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите слово 'Calories' чтобы начать")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
