import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()


def main_menu():
    kb = InlineKeyboardBuilder()

    kb.button(text="🛍 Каталог", callback_data="catalog")
    kb.button(text="👤 Профиль", callback_data="profile")
    kb.button(text="📦 Мои заказы", callback_data="orders")
    kb.button(text="💬 Поддержка", callback_data="support")

    kb.adjust(2)

    return kb.as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Выбери нужный раздел:",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "catalog")
async def catalog(call: CallbackQuery):
    kb = InlineKeyboardBuilder()

    kb.button(text="📦 Товар 1 — 10 ₽", callback_data="product1")
    kb.button(text="📦 Товар 2 — 20 ₽", callback_data="product2")
    kb.button(text="📦 Товар 3 — 30 ₽", callback_data="product3")
    kb.button(text="⬅️ Назад", callback_data="home")

    kb.adjust(1)

    await call.message.edit_text(
        "🛍 КАТАЛОГ\n\nВыбери товар:",
        reply_markup=kb.as_markup()
    )

    await call.answer()


@dp.callback_query(F.data.startswith("product"))
async def product(call: CallbackQuery):
    products = {
        "product1": ("Товар 1", 10),
        "product2": ("Товар 2", 20),
        "product3": ("Товар 3", 30),
    }

    name, price = products[call.data]

    kb = InlineKeyboardBuilder()
    kb.button(text="🛒 Купить", callback_data=f"buy:{call.data}")
    kb.button(text="⬅️ Каталог", callback_data="catalog")

    await call.message.edit_text(
        f"📦 {name}\n\n"
        f"💰 Цена: {price} ₽\n\n"
        "Нажми кнопку ниже, чтобы оформить заказ.",
        reply_markup=kb.as_markup()
    )

    await call.answer()


@dp.callback_query(F.data.startswith("buy:"))
async def buy(call: CallbackQuery):
    await call.message.edit_text(
        "✅ Заявка на заказ создана!\n\n"
        "Администратор свяжется с тобой для оформления.",
        reply_markup=main_menu()
    )

    await call.answer()


@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    await call.message.edit_text(
        f"👤 ПРОФИЛЬ\n\n"
        f"Telegram ID: {call.from_user.id}\n\n"
        "💰 Баланс: 0 ₽",
        reply_markup=main_menu()
    )

    await call.answer()


@dp.callback_query(F.data == "orders")
async def orders(call: CallbackQuery):
    await call.message.edit_text(
        "📦 МОИ ЗАКАЗЫ\n\n"
        "У тебя пока нет заказов.",
        reply_markup=main_menu()
    )

    await call.answer()


@dp.callback_query(F.data == "support")
async def support(call: CallbackQuery):
    await call.message.edit_text(
        "💬 ПОДДЕРЖКА\n\n"
        "По вопросам заказа обратись к администратору.",
        reply_markup=main_menu()
    )

    await call.answer()


@dp.callback_query(F.data == "home")
async def home(call: CallbackQuery):
    await call.message.edit_text(
        "🏠 Главное меню:",
        reply_markup=main_menu()
    )

    await call.answer()


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
