import logging
import config
import keyboard
import words

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())


class GetStateControl(StatesGroup):
    waiting_for_get_pair = State()


class LearnStateControl(StatesGroup):
    waiting_for_answer = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Выбери режим", reply_markup=keyboard.start_keyboard)


@dp.message_handler(commands=["help"])
async def get_random(message: types.Message):
    await message.answer("Для начала работы с ботом введите команду /start\n"
                         "Слова вводятся в формате Слово/перевод\n"
                         "Если нужно ввести два слово используй символ нижнее подчеркивание _\n"
                         "Например: auricula ушная_раковина")


@dp.message_handler(commands=["clr"])
async def delete_all_words(message: types.Message):
    if words.clean_database():
        await message.answer("Очищено")
    else:
        await message.answer("Невозможно выполнить")


@dp.message_handler(lambda message: message.text == "Добавить слова", state='*')
async def add_start(message: types.Message):
    await message.answer("Ввод слов осуществляется в формате lat ru\n"
                         "Если нужно ввести два слово используй символ нижнее подчеркивание _ ",
                         reply_markup=keyboard.cancel_keyboard)
    await GetStateControl.waiting_for_get_pair.set()


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(lambda message: message.text == "Отмена", state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=GetStateControl.waiting_for_get_pair, content_types=types.ContentTypes.TEXT)
async def add_step_next(message: types.Message):
    if words.add_word_pair(message.text):
        await message.answer("Добавлено")
    else:
        await message.answer("Слово Пробел слово")

    await GetStateControl.waiting_for_get_pair.set()


@dp.message_handler(lambda message: message.text == "Учить слова")
async def learn_chose(message: types.Message):
    await message.answer("Как будем учить???", reply_markup=keyboard.learn_keyboard)


@dp.message_handler(lambda message: message.text == "Слово - перевод", state='*')
async def learn_wt_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pair'] = words.get_random_pair()
    await LearnStateControl.waiting_for_answer.set()
    await message.answer(data['pair'][0], reply_markup=keyboard.cancel_keyboard)


@dp.message_handler(lambda message: message.text == "Перевод - слово", state='*')
async def learn_tw_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pair'] = words.get_random_pair()
    await LearnStateControl.waiting_for_answer.set()
    await message.answer(data['pair'][1], reply_markup=keyboard.cancel_keyboard)


@dp.message_handler(state=LearnStateControl.waiting_for_answer, content_types=types.ContentTypes.TEXT)
async def learn_wt_step_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != data['pair'][1]:
            await message.answer("Не верно", reply_markup=keyboard.cancel_keyboard)
        else:
            data['pair'] = words.get_random_pair()
            await message.answer("Верно\n" "Следующее слово:", reply_markup=keyboard.cancel_keyboard)
            await message.answer(data['pair'][0], reply_markup=keyboard.cancel_keyboard)
    await LearnStateControl.waiting_for_answer.set()


@dp.message_handler(state=LearnStateControl.waiting_for_answer, content_types=types.ContentTypes.TEXT)
async def learn_tw_step_next(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != data['pair'][0]:
            await message.answer("Не верно", reply_markup=keyboard.cancel_keyboard)
        else:
            data['pair'] = words.get_random_pair()
            await message.answer("Верно\n" "Следующее слово:", reply_markup=keyboard.cancel_keyboard)
            await message.answer(data['pair'][1], reply_markup=keyboard.cancel_keyboard)
    await LearnStateControl.waiting_for_answer.set()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
