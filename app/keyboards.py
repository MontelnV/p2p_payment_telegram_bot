from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = [
    [InlineKeyboardButton(text="Перейти в магазин", callback_data="go_to_pay")]
]
main_keyboard = InlineKeyboardMarkup(inline_keyboard=main_keyboard)

pay_keyboard = [
    [InlineKeyboardButton(text="Продукт за 1₽", callback_data="pay_1")],
    [InlineKeyboardButton(text="Продукт за 10₽", callback_data="pay_10")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
]
pay_keyboard = InlineKeyboardMarkup(inline_keyboard=pay_keyboard)
