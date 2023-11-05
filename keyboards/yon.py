from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.translations import _

def y(case_id, lang):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=_("Да", lang),
        callback_data=f"{case_id}:Yes")
    )
    builder.add(InlineKeyboardButton(
        text=_("Нет", lang),
        callback_data=f"{case_id}:No")
    )
    return builder.as_markup()

