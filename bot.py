import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
tasks = {}

class TaskStates(StatesGroup):
    waiting_for_task = State()
    waiting_for_done = State()
    waiting_for_delete = State()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить"), KeyboardButton(text="Список")],
        [KeyboardButton(text="Выполнено"), KeyboardButton(text="Удалить")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    tasks[message.from_user.id] = []
    await message.answer("Привет! Я помогу управлять твоими задачами.\nВыбери действие:", reply_markup=keyboard)

@dp.message(F.text == "Добавить")
async def add_task_start(message: types.Message, state: FSMContext):
    """Запрашивает текст новой задачи."""
    await state.set_state(TaskStates.waiting_for_task)
    await message.answer("Введи текст задачи:")

@dp.message(TaskStates.waiting_for_task)
async def add_task_finish(message: types.Message, state: FSMContext):
    """Сохраняет новую задачу в список."""
    user_id = message.from_user.id
    if user_id not in tasks:
        tasks[user_id] = []
    tasks[user_id].append({"text": message.text, "done": False})
    await state.clear()
    await message.answer("Задача добавлена!", reply_markup=keyboard)

@dp.message(F.text == "Список")
async def show_tasks(message: types.Message):
    """Показывает список всех задач пользователя."""
    user_id = message.from_user.id
    if user_id not in tasks or not tasks[user_id]:
        await message.answer("У тебя пока нет задач.")
        return
    result = "Твои задачи:\n"
    for i, task in enumerate(tasks[user_id], 1):
        icon = "[+]" if task["done"] else "[ ]"
        result += f"{i}. {icon} {task['text']}\n"
    await message.answer(result)

@dp.message(F.text == "Выполнено")
async def mark_done_start(message: types.Message, state: FSMContext):
    """Запрашивает номер задачи для отметки выполненной."""
    user_id = message.from_user.id
    if user_id not in tasks or not tasks[user_id]:
        await message.answer("У тебя пока нет задач.")
        return
    await state.set_state(TaskStates.waiting_for_done)
    await message.answer("Введи номер выполненной задачи:")

@dp.message(TaskStates.waiting_for_done)
async def mark_done_finish(message: types.Message, state: FSMContext):
    """Отмечает задачу как выполненную."""
    user_id = message.from_user.id
    try:
        index = int(message.text) - 1
        tasks[user_id][index]["done"] = True
        await state.clear()
        await message.answer("Задача выполнена!", reply_markup=keyboard)
    except (ValueError, IndexError):
        await message.answer("Неверный номер, попробуй снова:")

@dp.message(F.text == "Удалить")
async def delete_task_start(message: types.Message, state: FSMContext):
    """Запрашивает номер задачи для удаления."""
    user_id = message.from_user.id
    if user_id not in tasks or not tasks[user_id]:
        await message.answer("У тебя пока нет задач.")
        return
    await state.set_state(TaskStates.waiting_for_delete)
    await message.answer("Введи номер задачи для удаления:")

@dp.message(TaskStates.waiting_for_delete)
async def delete_task_finish(message: types.Message, state: FSMContext):
    """Удаляет задачу из списка."""
    user_id = message.from_user.id
    try:
        index = int(message.text) - 1
        tasks[user_id].pop(index)
        await state.clear()
        await message.answer("Задача удалена!", reply_markup=keyboard)
    except (ValueError, IndexError):
        await message.answer("Неверный номер, попробуй снова:")

async def main():
    """Запуск бота."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())