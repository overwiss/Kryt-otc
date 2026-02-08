import asyncio
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

# --- НАСТРОЙКИ ---
bot = Bot(token="8531227508:AAH0hraNjR-yS7_NHj4T29osDXgiqshYO38")
dp = Dispatcher()

ADMIN_ID = 7634507602
BANNER_URL = "https://s4.iimage.su/s/08/ge2Mdk3xsEJWX46gzz9mR2PtIurOfg5mz6VqTiJ1.jpg"
MANAGER_CARD = "2204 1201 3279 4013 - Маркин Ярослав"
SUPPORT_URL = "https://t.me/FunPaySupportOTC"

# Хранение данных
user_languages = {}
user_deals = {}
active_deals = {}
user_balances = {} # Для профиля
user_agreements = {}

def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        await callback.message.answer(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# --- КЛАВИАТУРЫ ---

# 1. Выбор языка
lang_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
     InlineKeyboardButton(text="🇺🇸 English", callback_data="set_lang_en")]
])

# 2. Правила
def get_start_keyboard(lang):
    text = "✅ Я согласен с правилами" if lang == "ru" else "✅ I agree to the rules"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data="agree")]])

# 3. Главное меню
def get_main_menu(lang):
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛡️ Создать сделку", callback_data="create_deal")],
            [InlineKeyboardButton(text="👤 Профиль", callback_data="profile"), InlineKeyboardButton(text="💳 Реквизиты", callback_data="requisites")],
            [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="change_lang")],
            [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot"), InlineKeyboardButton(text="📞 Поддержка", url=SUPPORT_URL)],
            [InlineKeyboardButton(text="🌐 Наш сайт", url="https://funpay.com/")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛡️ Create deal", callback_data="create_deal")],
            [InlineKeyboardButton(text="👤 Profile", callback_data="profile"), InlineKeyboardButton(text="💳 Requisites", callback_data="requisites")],
            [InlineKeyboardButton(text="🌍 Change Language", callback_data="change_lang")],
            [InlineKeyboardButton(text="ℹ️ About", callback_data="about_bot"), InlineKeyboardButton(text="📞 Support", url=SUPPORT_URL)],
            [InlineKeyboardButton(text="🌐 Our Website", url="https://funpay.com/")]
        ])

# 4. Валюты (Все твои + Stars)
currency_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="curr_RUB"), InlineKeyboardButton(text="🇺🇸 USD", callback_data="curr_USD")],
    [InlineKeyboardButton(text="🇪🇺 EUR", callback_data="curr_EUR"), InlineKeyboardButton(text="🇺🇿 UZS", callback_data="curr_UZS")],
    [InlineKeyboardButton(text="🇰🇬 KGS", callback_data="curr_KGS"), InlineKeyboardButton(text="🇰🇿 KZT", callback_data="curr_KZT")],
    [InlineKeyboardButton(text="🇧🇾 BYN", callback_data="curr_BYN"), InlineKeyboardButton(text="🇺🇦 UAH", callback_data="curr_UAH")],
    [InlineKeyboardButton(text="💎 TON", callback_data="curr_TON"), InlineKeyboardButton(text="⭐️ Stars", callback_data="curr_Stars")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="curr_USDT")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

# --- ОБРАБОТКА КОМАНД ---

@dp.message(CommandStart())
async def start_cmd(message: Message):
    user_id = message.from_user.id
    if user_id in user_deals: del user_deals[user_id]
    await message.answer("Выберите язык / Choose language:", reply_markup=lang_keyboard)

@dp.message(Command("hostlebuy"))
async def hostlebuy_cmd(message: Message):
    args = message.text.split()
    if len(args) < 2: return
    d_id = args[1].lower().replace("#", "")
    if d_id in active_deals:
        deal = active_deals[d_id]
        await message.answer(f"✅ Оплата сделки #{d_id} принята!")
        try:
            await bot.send_message(deal["seller_id"], f"💰 Покупатель оплатил сделку #{d_id}! Передайте товар.")
        except: pass
    else:
        await message.answer("❌ Сделка не найдена.")

# --- CALLBACKS ---

@dp.callback_query()
async def cb_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    data = callback.data

    if data.startswith("set_lang_"):
        user_languages[user_id] = data.split("_")[2]
        lang = user_languages[user_id]
        rules = ("<b>Правила FunPay OTC:</b>\n1. Будьте вежливы.\n2. Сделки только через бота.\n3. Не передавайте контакты." 
                 if lang == "ru" else "<b>Rules:</b>\n1. Be polite.\n2. Deals only via bot.\n3. Don't share contacts.")
        await safe_edit_message(callback, rules, get_start_keyboard(lang))

    elif data == "agree" or data == "back_to_menu":
        if user_id in user_deals: del user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        caption = "🎁 <b>FunPay OTC | Главное меню</b>" if lang == "ru" else "🎁 <b>FunPay OTC | Main Menu</b>"
        await bot.send_photo(user_id, photo=BANNER_URL, caption=caption, reply_markup=get_main_menu(lang), parse_mode=ParseMode.HTML)

    elif data == "create_deal":
        user_deals[user_id] = {"step": "desc"}
        lang = user_languages.get(user_id, "ru")
        await callback.message.answer("📝 Введите описание товара:" if lang == "ru" else "📝 Enter item description:")

    elif data == "profile":
        lang = user_languages.get(user_id, "ru")
        balance = user_balances.get(user_id, 0.0)
        text = f"👤 <b>Профиль</b>\n\n🆔 ID: <code>{user_id}</code>\n💰 Баланс: {balance} RUB" if lang == "ru" else f"👤 <b>Profile</b>\n\n🆔 ID: <code>{user_id}</code>\n💰 Balance: {balance} RUB"
        await callback.message.answer(text, parse_mode=ParseMode.HTML)

    elif data == "requisites":
        lang = user_languages.get(user_id, "ru")
        text = f"💳 <b>Наши реквизиты:</b>\n<code>{MANAGER_CARD}</code>" if lang == "ru" else f"💳 <b>Our Requisites:</b>\n<code>{MANAGER_CARD}</code>"
        await callback.message.answer(text, parse_mode=ParseMode.HTML)

    elif data == "about_bot":
        lang = user_languages.get(user_id, "ru")
        text = "🤖 <b>О боте</b>\nFunPay OTC — лучший бот для безопасных сделок." if lang == "ru" else "🤖 <b>About</b>\nFunPay OTC — best bot for safe deals."
        await callback.message.answer(text, parse_mode=ParseMode.HTML)

    elif data == "change_lang":
        await callback.message.answer("Выберите язык:", reply_markup=lang_keyboard)

    elif data.startswith("curr_"):
        if user_id in user_deals:
            user_deals[user_id]["currency"] = data.split("_")[1]
            user_deals[user_id]["step"] = "amount"
            lang = user_languages.get(user_id, "ru")
            await callback.message.answer(f"💰 Введите сумму ({user_deals[user_id]['currency']}):")

# --- TEXT ---

@dp.message(F.text)
async def text_handler(message: Message):
    user_id = message.from_user.id
    if user_id in user_deals:
        state = user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        
        if state["step"] == "desc":
            state["desc"] = message.text
            state["step"] = "curr"
            await message.answer("Выберите валюту:" if lang == "ru" else "Choose currency:", reply_markup=currency_keyboard)
            
        elif state["step"] == "amount":
            try:
                amt = float(message.text.replace(",", "."))
                d_id = generate_deal_id()
                active_deals[d_id] = {"seller_id": user_id, "amount": amt, "currency": state["currency"]}
                link = f"https://t.me/{(await bot.get_me()).username}?start=deal_{d_id}"
                await message.answer(f"✅ <b>Сделка создана!</b>\nID: {d_id}\nСсылка: {link}" if lang == "ru" else f"✅ <b>Deal created!</b>\nID: {d_id}\nLink: {link}", parse_mode=ParseMode.HTML)
                del user_deals[user_id]
            except:
                await message.answer("❌ Введите число!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())