from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR, IS_ADMIN, IS_MEMBER
from aiogram.types import Message, ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from states.states import PollState
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from db import NewPeopleMembers, NewCase, NewPeopleChats, MemberReason 
from sqlalchemy.orm import selectinload
from .translations import _


# Создание объекта маршрутизатора для обработки команд и сообщений
router = Router(name="starting-router")

# Словарь, используемый для отображения типов чатов в текстовые описания
chats_variants = {
    "group": "группу",
    "supergroup": "супергруппу"
}

# Список всех возможных первых цифр номера телефона
all_numbers = ["8771", "8707", "8747", "8776", "8777", "8700", "8708", "8702", "8778", "8701", "8705", "8775", "8706"]

# Обработчик события: бот был добавлен в чат как участник
@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot, session: AsyncSession):
    # Проверяем, есть ли у бота разрешение на отправку сообщений в чат
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        # Если разрешение есть, отправляем приветственное сообщение и добавляем чат в базу данных
        await bot.send_message(chat_id=event.chat.id,
            text="Салеметсіздер ме? Қосқандарыңызға рахмет\nЗдравствуйте, Спасибо что добавили"
        )
        chat = NewPeopleChats(
            chat_id = event.chat.id, 
        )
        session.add(chat)
        await session.commit()
    else:
        print("Как-нибудь логируем эту ситуацию")



# Обработчик команды "/start" в личном чате пользователя
@router.message(Command("start"), F.chat.type == 'private')
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    # Проверяем, есть ли пользователь в базе данных
    user = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == message.from_user.id))
    user = user.scalar()
    if user: 
        # Если пользователь найден, отправляем приветственное сообщение с его именем
        await message.answer(f"{_('Привет', user.language)}, {user.name}")
    else:
        # Если пользователь не найден, начинаем процесс опроса, запрашивая имя
        await state.set_state(PollState.language)
        await message.answer("Привет, Выбери язык\nСәлем, Тілді таңданыз", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="kz"),
                    KeyboardButton(text="ru"),
                ]
            ],
            resize_keyboard=True,
        ),)

@router.message(PollState.language)
async def process_lang(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(language=message.text)
    await state.set_state(PollState.name)
    await message.answer(_("Привет, Как тебя зовут? (Фамилия и Имя)", message.text), reply_markup=ReplyKeyboardRemove())


# Обработчик для состояния PollState.name: ожидание имени пользователя
@router.message(PollState.name)
async def process_name(message: Message, state: FSMContext) -> None:
    # Обновляем данные состояния с именем пользователя и переходим к следующему состоянию
    data = await state.update_data(name=message.text)
    await state.set_state(PollState.phone_number)
    await message.answer(
        _("Отлично, Напиши свой номер телефона начиная с 8", data['language'])
    )

# Обработчик для состояния PollState.phone_number: ожидание номера телефона пользователя
@router.message(PollState.phone_number, (F.text[0:4].in_(all_numbers)) & (F.text.len() == 11) & (F.text.isdigit()))
async def process_number(message: Message, state: FSMContext) -> None:
    # Если введенный номер телефона соответствует требованиям, обновляем данные состояния и переходим к следующему состоянию
    data = await state.update_data(phone_number=message.text)
    await state.set_state(PollState.th_text)
    await message.answer(_("Коротко опишите ваше мнение по поводу проекта «Жана Адамдар»:", data['language']))

# Обработчик для состояния PollState.phone_number в случае ошибочного ввода номера телефона
@router.message(PollState.phone_number)
async def process_number_error(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(_("Вы ввели неправильный номер", data['language']))

# Обработчик для состояния PollState.th_text: ожидание текста мнения пользователя по проекту
@router.message(PollState.th_text)
async def process_th_text(message: Message, state: FSMContext) -> None:
    # Обновляем данные состояния с текстом мнения пользователя и переходим к следующему состоянию
    data = await state.update_data(th_text=message.text)
    await state.set_state(PollState.sg_text)
    await message.answer(
        _("Что, на ваш взгляд, не хватает проекту «Жана Адамдар»? Чем его дополнить?", data['language'])
    )


# Обработчик для состояния PollState.sg_text: ожидание текста предложений по улучшению проекта
@router.message(PollState.sg_text)
async def process_sg_text(message: Message, state: FSMContext) -> None:
    # Обновляем данные состояния с текстом предложений и переходим к следующему состоянию
    data = await state.update_data(sg_text=message.text)
    await state.set_state(PollState.yon)
    # Запрашиваем у пользователя желание присоединиться к движению с вариантами ответа "Да" или "Нет"
    await message.answer(
        _("Вы хотите присоединиться к движению «Жана Адамдар»?", data['language']), 
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=_("Да", data["language"])),
                    KeyboardButton(text=_("Нет", data["language"])),
                ]
            ],
            resize_keyboard=True,
        ),
    )

# Обработчик для ответа "Да" в состоянии PollState.yon
@router.message(PollState.yon, (F.text.in_({"Да", "Иа"})))
async def process_yon_y(message: Message, state: FSMContext, session: AsyncSession) -> None:
    # Обновляем данные состояния с ответом пользователя "Да" и сохраняем информацию в базе данных
    data = await state.update_data(yon="Да")

    user = NewPeopleMembers(

        user_id = message.from_user.id, 
        name = data["name"], 
        phone_number = int(data["phone_number"]),
        th_text = data["th_text"],
        sg_text = data["sg_text"], 
        yon = data['yon']
    )
    session.add(user)
    await session.commit()
    await state.clear()
    await message.answer(
        _("Отлично, я все записал. Здесь вы будете получать уведомления", data['language']),
        reply_markup=ReplyKeyboardRemove(),
    )

# Обработчик для ответа "Нет" в состоянии PollState.yon
@router.message(PollState.yon, F.text.in_({"Нет", "Жоқ"}))
async def process_yon_n(message: Message, state: FSMContext, session: AsyncSession) -> None:
    # Обновляем данные состояния с ответом пользователя "Нет" и сохраняем информацию в базе данных
    data = await state.update_data(yon="Нет")
    user = NewPeopleMembers(
        user_id = message.from_user.id, 
        name = data["name"], 
        phone_number = int(data["phone_number"]),
        th_text = data["th_text"],
        sg_text = data["sg_text"], 
        yon = data['yon']
    )
    session.add(user)
    await session.commit()
    await state.clear()
    # Отправляем прощальное сообщение пользователю
    await message.reply(
        _("Отлично, я все записал. Пока!", data['language']),
        reply_markup=ReplyKeyboardRemove(),
    )

# Обработчик команды "/help"
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Этот бот создан чтобы информировать о предстоящих мероприятиях.")
