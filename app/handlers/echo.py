from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from states.register import Register
from database.postgres import conn

echo_router = Router()
conn = conn()
cur = conn.cursor()

@echo_router.message(Command("register"))
async def register(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Register.ism)

@echo_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Botga xush kelibsiz!")

@echo_router.message(Register.ism)
async def get_ism(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer("Shahringizni kiriting:")
    await state.set_state(Register.shahar)

@echo_router.message(Register.shahar)
async def get_shahar(message: types.Message, state: FSMContext):
    await state.update_data(shahar=message.text)
    await message.answer("Kasbingizni kiriting:")
    await state.set_state(Register.kasb)

@echo_router.message(Register.kasb)
async def get_kasb(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id

    await state.update_data(kasb=message.text)
    data = await state.get_data()

    ism = data.get("ism")
    shahar = data.get("shahar")
    kasb = data.get("kasb")

    cur.execute("INSERT INTO users (chat_id, ism, shahar, kasb) VALUES (%s, %s, %s, %s)",(chat_id, ism, shahar, kasb))
    conn.commit()

    await message.answer(f"Ro'yxatdan o'tdingiz: {ism}, {shahar}, {kasb}")
    await state.clear()