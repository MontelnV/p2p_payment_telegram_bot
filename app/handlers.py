import os, string, random
import app.keyboards as kb

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from yoomoney import Quickpay, Client
from app.repositories import UserRepository
from dotenv import load_dotenv

load_dotenv()
router = Router()

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    user_id = message.from_user.id

    await UserRepository.add_user_to_sendlist(user_id=user_id) # добавить пользователя в лист рассылки

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text="Этот бот - маленькая копия интернет-магазина для демонстрации возможностей использования P2P-платежей в реальной работе (на примере кошелька ЮMoney)", reply_markup=kb.main_keyboard)

@router.callback_query(lambda call: call.data == "go_to_pay")
async def pay(callback: CallbackQuery):
    await callback.message.answer(text="Пожалуйста, выберите продукт который хотите приобрести", reply_markup=kb.pay_keyboard)

@router.callback_query(lambda call: call.data == "back")
async def back(callback: CallbackQuery):
    await callback.message.delete()

# ------------------------------------------ #

@router.callback_query(F.data.startswith('pay_'))
async def handle_payment(callback: CallbackQuery):

    cost = callback.data.split('_')[1]
    user_id = callback.from_user.id
    username = callback.from_user.username if callback.from_user.username is not None else None

    letters_and_digits = string.ascii_lowercase + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, 10)) # случайный уникальный лейбл платежа

    quickpay = Quickpay(
        receiver='your_account_number', # номер счёта yoomoney на который зачисляются деньги формата 4100XXXXXXXXXXXX
        quickpay_form='button',
        targets='Testing', # название приложения которое вы ввели при его регистрации
        paymentType='SB', # оплата либо с карты, либо с самого кошелька
        sum=cost, # цена которая прилетает из callback-клавиатуры
        label=rand_string, # случайный набор символов (UUID платежа)
        successURL="https://t.me/your_bot" # ссылка на ваше приложение для перехода обратно в магазин после успешной оплаты
    )

    await UserRepository.add_transaction(user_id=user_id, label=rand_string, subscribe_type=cost, username=username) # добавление транзакции в базу данных

    # основная клавиатура для оплаты
    main_pay_keyboard = [
            [InlineKeyboardButton(text='Оплатить', url=quickpay.redirected_url)],
            [InlineKeyboardButton(text="Я оплатил", callback_data=f"claim_{rand_string}")]
    ]
    main_pay_keyboard = InlineKeyboardMarkup(inline_keyboard=main_pay_keyboard)
    # ---------------------------------#

    await callback.message.answer(parse_mode="HTML", text=f"Выбран продукт за <b>{cost}₽</b>\n\nЕсли вы не купили продукт, то нажмите на кнопку <b>Оплатить</b> и выполните оплату, а затем нажмите на кнопку <b>Я оплатил</b>\n\nЕсли вы уже купили продукт, то нажмите на кнопку <b>Я оплатил</b>", reply_markup=main_pay_keyboard)

# роутер для оплаты товара
@router.callback_query(F.data.startswith('claim_'))
async def check_payment(callback: CallbackQuery, bot: Bot):
    callback_data = callback.data
    rand_string = callback_data.split('_')[1]
    data = await UserRepository.get_payment_status(callback.from_user.id, label=rand_string)
    if not data:
        await callback.message.answer(parse_mode="HTML", text="<b>Такого платежа не существует! Возможно он уже был произведен и находится в пути или ссылка недейстивтельна!</b>")
    else:
        check = data[0].check
        label = data[0].label
        date = data[0].created_at
        subscribe_type = data[0].subscribe_type
        if check == False:
            client = Client(os.getenv("PAYMENT_P2P"))
            history = client.operation_history(label=label)
            try:
                operation = history.operations[-1]
                if operation.status == 'success':
                    await UserRepository.update_payment_status(user_id=callback.from_user.id, label=label, subscribe_type=subscribe_type)
                    await callback.message.answer(parse_mode="HTML", text="<b>Оплата прошла успешно! Сообщение отправлено менеджеру!</b>")
                    await bot.send_message(chat_id="your-chat-id", text=f"Пользователь {callback.from_user.id} с аккаунта @{callback.from_user.username} приобрел продукт за {subscribe_type} рублей {date.date()} в {date.time().strftime('%H:%M')} МСК")

                    # удаление транзакции после успешной проверки (можно и оставлять об этом запись, на ваше усмотрение)
                    await UserRepository.delete_transaction(user_id=callback.from_user.id, label=label, subscribe_type=subscribe_type)
            except Exception as e:
                await callback.message.answer(parse_mode="HTML", text="<b>Вы не оплатили продукт или оплата еще в пути!</b>")

        else:
            await callback.message.answer(parse_mode="HTML", text="<b>Оплата прошла успешно! Сообщение отправлено менеджеру!</b>")
            await bot.send_message(chat_id="your-chat-id", text=f"Пользователь {callback.from_user.id} с аккаунта @{callback.from_user.username} приобрел продукт за {subscribe_type} рублей {date.date()} в {date.time().strftime('%H:%M')} МСК")

            # удаление транзакции после успешной проверки (можно и оставлять об этом запись, на ваше усмотрение)
            await UserRepository.delete_transaction(user_id=callback.from_user.id, label=label, subscribe_type=subscribe_type)
