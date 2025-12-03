import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yookassa import Configuration, Payment

logging.basicConfig(level=logging.INFO)

# ---------- ТВОИ ДАННЫЕ ----------
BOT_TOKEN = "8308942169:AAGJL-mF-9Ig0HrKFHwGaATP-FqBvKStpO4"
SHOP_ID = "1220442"
SHOP_SECRET_KEY = "test"     # У тестового магазина секретный ключ = test
CHANNEL_ID = -1003328408384
PRICE_RUB = 1500
PROMOCODE = "FIRSTMONTH"
ADMIN_ID = 405491563   # Поставь сюда свой Telegram ID вместо токена бота
# ---------------------------------

# Юкасса
Configuration.account_id = SHOP_ID
Configuration.secret_key = SHOP_SECRET_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище подписок в оперативной памяти (на Render будет работать нормально)
users = {}  # {user_id: {"expires": date}}

# ---------- Кнопки ----------
def get_pay_keyboard(payment_url):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 1500₽", url=payment_url)]
    ])
    return kb

# ---------- Команда /start ----------
@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в *Твоя Математика*!\n\n"
        "Цена подписки: 1500 ₽ / 30 дней.\n"
        "Промокод на скидку 50%: FIRSTMONTH\n\n"
        "Чтобы оформить подписку, нажмите:\n /pay",
        parse_mode="Markdown"
    )

# ---------- Оплата ----------
@dp.message(F.text == "/pay")
async def pay(message: types.Message):
    user_id = message.from_user.id

    # Проверяем срок подписки
    if user_id in users:
        if users[user_id]["expires"] > datetime.now():
            remain = users[user_id]["expires"] - datetime.now()
            days = remain.days
            return await message.answer(f"У тебя есть активная подписка: ещё {days} дней.")

    await message.answer("Введи промокод или отправь '-' если промокода нет.")

# ---------- Приём промокода ----------
@dp.message(lambda m: m.text.lower() == PROMOCODE.lower() or m.text == "-")
async def promo_handler(message: types.Message):
    user_id = message.from_user.id

    promo_used = message.text.lower() == PROMOCODE.lower()

    cost = PRICE_RUB
    if promo_used:
        cost = PRICE_RUB // 2

    # Создаем платёж
    payment = Payment.create({
        "amount": {"value": str(cost), "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": "https://t.me/tvyamatematika"},
        "capture": True,
        "description": f"Оплата подписки {user_id}"
    })

    pay_url = payment.confirmation.confirmation_url
    payment_id = payment.id

    users[user_id] = {"payment_id": payment_id}   # только для отслеживания

    await message.answer(
        f"Цена: {cost} ₽.\n\nЖми кнопку для оплаты:",
        reply_markup=get_pay_keyboard(pay_url)
    )

# ---------- Вебхук Юкассы (Псевдо — Render примет через polling) ----------
async def check_payments():
    while True:
        now = datetime.now()
        for user, data in list(users.items()):
            if "payment_id" in data:
                try:
                    payment = Payment.find_one(data["payment_id"])
                    if payment.status == "succeeded":
                        users[user]["expires"] = now + timedelta(days=30)
                        users[user].pop("payment_id")

                        # выдача приглашения
                        invite = await bot.create_chat_invite_link(CHANNEL_ID, member_limit=1)
                        await bot.send_message(
                            user,
                            "Оплата прошла успешно!\nВот ваша ссылка на закрытый канал:",
                        )
                        await bot.send_message(user, invite.invite_link)
                except:
                    pass
        await asyncio.sleep(5)

# ---------- Админ-панель ----------
@dp.message(F.text == "/admin")
async def admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer
OLXTOTO » Bandar Togel Online Resmi Dan Paito Warna Sdy Hari Ini
OLXTOTO » Bandar Togel Online Resmi Dan Paito Warna Sdy Hari Ini
www.franklinspaine.com


"Админ-панель:\n"
        "/subscribers — список подписчиков"
    )

@dp.message(F.text == "/subscribers")
async def subs(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = "Подписчики:\n"
    for user, data in users.items():
        if "expires" in data:
            text += f"{user} — до {data['expires']}\n"
    await message.answer(text)

# ---------- Main ----------
async def main():
    asyncio.create_task(check_payments())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())(