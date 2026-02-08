import asyncio
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

# Данные бота
bot = Bot(token="8531227508:AAH0hraNjR-yS7_NHj4T29osDXgiqshYO38")
dp = Dispatcher()

# Хранение данных
user_agreements = {}
user_deals = {}
active_deals = {}
MANAGER_CARD = "2204 1201 3279 4013 - Маркин Ярослав"
BANNER_URL = "https://s4.iimage.su/s/08/ge2Mdk3xsEJWX46gzz9mR2PtIurOfg5mz6VqTiJ1.jpg"

def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# --- КЛАВИАТУРЫ (ПОЛНЫЙ СПИСОК + STARS) ---
start_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Полностью согласен", callback_data="agree")]
])

main_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Создать сделку", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Реквизиты", callback_data="requisites")],
    [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/FunPaySupportOTC")]
])

currency_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="curr_RUB"), InlineKeyboardButton(text="🇺🇸 USD", callback_data="curr_USD")],
    [InlineKeyboardButton(text="🇪🇺 EUR", callback_data="curr_EUR"), InlineKeyboardButton(text="🇺🇿 UZS", callback_data="curr_UZS")],
    [InlineKeyboardButton(text="🇰🇬 KGS", callback_data="curr_KGS"), InlineKeyboardButton(text="🇰🇿 KZT", callback_data="curr_KZT")],
    [InlineKeyboardButton(text="🇧🇾 BYN", callback_data="curr_BYN"), InlineKeyboardButton(text="🇺🇦 UAH", callback_data="curr_UAH")],
    [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON"), InlineKeyboardButton(text="💰 USDT", callback_data="curr_USDT")],
    [InlineKeyboardButton(text="⭐️ Stars", callback_data="curr_Stars")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

seller_confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Товар отправлен", callback_data="item_sent")]
])

# --- КОМАНДЫ ---

@dp.message(CommandStart())
async def start_cmd(message: Message):
    user_id = message.from_user.id
    if user_id in user_deals: del user_deals[user_id]
    
    await message.answer(
        "<b>🎁 Добро пожаловать в Funpay OTC!</b>\n\n"
        "Правила сервиса:\n"
        "1. Работа только через Гарант-сервис.\n"
        "2. Оскорбления и спам запрещены.\n\n"
        "Вы согласны с правилами?", 
        reply_markup=start_keyboard_ru, 
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("hostlebuy"))
async def hostlebuy_cmd(message: Message):
    args = message.text.split()
    if len(args) < 2: return
    
    deal_id = args[1].lower().replace("#", "")
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        buyer_ref = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        
        await message.answer(f"✅ Оплата сделки #{deal_id} принята!")
        await bot.send_message(
            deal["seller_id"], 
            f"💰 <b>Покупатель ({buyer_ref}) оплатил #{deal_id}!</b>\n\nПередайте товар и нажмите кнопку подтверждения.",
            reply_markup=seller_confirm_keyboard, parse_mode=ParseMode.HTML
        )
    else:
        await message.answer("❌ Сделка не найдена.")

# --- ОБРАБОТКА КНОПОК ---

@dp.callback_query()
async def cb_handler(callback: CallbackQuery):
    await callback.answer() # Исправляет зависание кнопок
    user_id = callback.from_user.id
    
    if callback.data == "agree":
        await callback.message.answer("🎉 Вы успешно зарегистрированы!", reply_markup=main_keyboard_ru)
        
    elif callback.data == "create_deal":
        user_deals[user_id] = {"step": "desc"}
        await callback.message.edit_text("📝 Введите описание товара:")

    elif callback.data == "back_to_menu":
        if user_id in user_deals: del user_deals[user_id]
        await bot.send_photo(user_id, photo=BANNER_URL, caption="🎁 <b>FunPay OTC | Меню</b>", reply_markup=main_keyboard_ru)

    elif callback.data.startswith("curr_"):
        if user_id in user_deals:
            user_deals[user_id]["currency"] = callback.data.split("_")[1]
            user_deals[user_id]["step"] = "amount"
            await callback.message.edit_text(f"💰 Введите сумму в {user_deals[user_id]['currency']}:")

# --- ОБРАБОТКА ТЕКСТА ---

@dp.message(F.text)
async def text_handler(message: Message):
    user_id = message.from_user.id
    if user_id in user_deals:
        state = user_deals[user_id]
        
        if state["step"] == "desc":
            state["desc"] = message.text
            state["step"] = "curr"
            await message.answer("Выберите валюту:", reply_markup=currency_keyboard_ru)
            
        elif state["step"] == "amount":
            if message.text.startswith("/"):
                del user_deals[user_id]
                return
            try:
                amount = float(message.text.replace(",", "."))
                d_id = generate_deal_id()
                active_deals[d_id] = {
                    "seller_id": user_id,
                    "amount": amount,
                    "currency": state["currency"]
                }
                bot_info = await bot.get_me()
                link = f"https://t.me/{bot_info.username}?start=deal_{d_id}"
                await message.answer(f"✅ Сделка создана!\n\nID: <code>{d_id}</code>\nСсылка: <code>{link}</code>", parse_mode=ParseMode.HTML)
                del user_deals[user_id]
            except:
                await message.answer("❌ Введите сумму числом.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())