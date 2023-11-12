from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.states import CaseState, DCome
from sqlalchemy.ext.asyncio import AsyncSession
from db import NewCase, NewPeopleMembers, NewPeopleChats, MemberReason 
from sqlalchemy import select, update, delete
import asyncio
from keyboards.yon import y
from sqlalchemy.orm import selectinload
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.exceptions import TelegramForbiddenError 
from .translations import _
import os
from aiogram.types import FSInputFile
from .translations import _
# Создание объекта маршрутизатора для обработки команд и сообщений
router = Router(name="admin-router")


@router.message(F.text == "GqaX8@c@c=8DJRc=0wpj4F]1#wZ)9YF~>!ciG4u}u5cQ)iV*qzrwN>y6_~_?].q@dZmtz]n@onEZ2DjBeEP)QJyyE.GdD,RU?W!ZHA")
async def cmd_admin_key(message: Message, session: AsyncSession):
    # Проверяем, есть ли пользователь в базе данных
    user = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == message.from_user.id))
    user = user.scalar()
    if user: 
        # Если пользователь найден, делаем его администратором
        user_change = update(NewPeopleMembers).where(NewPeopleMembers.user_id == message.from_user.id).values({NewPeopleMembers.is_admin: True})
        await session.execute(user_change)
        await session.commit()
        await message.answer(f"Привет, {user.name}. Теперь ты админ")
    else:
        await message.answer(f"Привет, тебя нет в базе")

# Обработчик для команды "/add" в личном чате администратора
@router.message(Command('add'), F.chat.type == 'private')
async def cmd_add_case(message: Message, state: FSMContext, session: AsyncSession):
    # Проверяем, является ли отправитель команды администратором
    user = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == message.from_user.id))
    user = user.scalar()
    if user: 
        # Если пользователь - администратор, устанавливаем состояние и ждем название дела
        if user.is_admin:
            await state.set_state(CaseState.to_who)
            await message.answer("Куда отправить?", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="chat"),
                    KeyboardButton(text="users"),
                ]
            ],
            resize_keyboard=True,
        ),)

# Обработчик для получения названия дела в состоянии CaseState.name
@router.message(CaseState.to_who)
async def to_who_handler(message: Message, state: FSMContext, bot:Bot):
    # Обновляем данные состояния с названием дела и переходим к следующему состоянию
    await state.update_data(to_who=message.text)
    await state.set_state(CaseState.name)
    await message.answer("Название:", reply_markup=ReplyKeyboardRemove())


@router.message(CaseState.name)
async def cmd_add_case_1(message: Message, state: FSMContext):
    # Обновляем данные состояния с названием дела и переходим к следующему состоянию
    await state.update_data(name=message.text)
    await state.set_state(CaseState.text)
    await message.answer("Отправь фотографию и текст (фото не обязательно)")

# Обработчик для получения фотографии и текста в состоянии CaseState.text с типом контента "photo"
@router.message(CaseState.text, F.content_type.in_({'photo'}))
async def cmd_add_case_2(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    # Получаем данные из состояния и создаем новый объект дела в базе данных
    user_count = await session.execute(select(NewPeopleMembers))
    dt = {
            'image_id': message.photo[0].file_id,
            'text': message.caption
        } 
    data = await state.update_data(text=dt)
    to_who = data['to_who']
    print(to_who)
    case = NewCase(
            name=data['name'],
            people_count=len(list(user_count)), 
            image = data['text']['image_id'],
            text = data['text']['text']
        )
    # Отправляем сообщения всем пользователям и чатам с делом и его маркапом
    user_count = await session.execute(select(NewPeopleMembers))
    session.add(case)
    await session.commit()
    await state.clear()
    if to_who == 'users':
        for user in user_count.scalars():
            try:
                await bot.send_photo(chat_id=int(user.user_id), photo=dt['image_id'], caption=dt['text'], reply_markup=y(case.case_id, user.language)) 
                await asyncio.sleep(0.05)
            except TelegramForbiddenError:
                pass
            except Exception as e:
                await asyncio.sleep(0.3)
                await bot.send_photo(chat_id=int(user.user_id), photo=dt['image_id'], caption=dt['text'], reply_markup=y(case.case_id, user.language)) 
    else:
        chat_count = await session.execute(select(NewPeopleChats))
        for chat in chat_count.scalars():
            try:
                await bot.send_message(chat_id=int(chat.chat_id), text=dt['text'])
                await asyncio.sleep(0.1)
            except:
                await asyncio.sleep(0.1)
    await message.answer(f"Ок, номер вашего дела: {case.case_id}, вы можете использовать команду /case id")

# Обработчик для получения текста в состоянии CaseState.text с типом контента "text"
@router.message(CaseState.text, F.content_type.in_({'text'}))
async def cmd_add_case_3(message: Message, state: FSMContext, session: AsyncSession, bot:Bot):
    # Получаем данные из состояния и создаем новый объект дела в базе данных
    user_count = await session.execute(select(NewPeopleMembers))
    dt = {
            'image_id': None,
            'text': message.text
        } 
    data = await state.update_data(text=dt)
    to_who = data['to_who']

    case = NewCase(
            name=data['name'],
            people_count=len(list(user_count)), 
            image = data['text']['image_id'],
            text = data['text']['text']
        )
    session.add(case)      
    await session.commit()
    await state.clear()
    user_count = await session.execute(select(NewPeopleMembers))
    # Отправляем сообщения всем пользователям и чатам с делом и его маркапом
    if to_who == 'users':
        for user in user_count.scalars():
            try:
                await bot.send_message(chat_id=int(user.user_id), text=dt['text'], reply_markup=y(case.case_id, user.language))
                await asyncio.sleep(0.05)
            except TelegramForbiddenError:
                pass
            except Exception as e:
                await asyncio.sleep(0.3)
                await bot.send_message(chat_id=int(user.user_id), text=dt['text'], reply_markup=y(case.case_id, user.language))
    else:
        chat_count = await session.execute(select(NewPeopleChats))
        for chat in chat_count.scalars():
            try:
                await bot.send_message(chat_id=int(chat.chat_id), text=dt['text'])
                asyncio.sleep(0.1)
            except Exception as e:
                asyncio.sleep(0.1)

    await message.answer(f"Номер вашего дела: {case.case_id}, вы можете использовать команду /case id")

# Обработчик для inline-кнопок в сообщениях с делами
@router.callback_query()
async def my_handler(callback: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    user = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == int(callback.from_user.id)))
    user = user.scalar()
    if callback.data.split(":")[1] == "Yes":
        # Если пользователь нажал "Да", добавляем его к участникам дела в базе данных
        case_id = callback.data.split(":")[0]
        case = await session.execute(select(NewCase).options(selectinload(NewCase.people_accepted)).where(NewCase.case_id == int(case_id)))
        case = case.scalar()
        case.people_accepted.append(user)
        session.add(case)
        await session.commit()
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id) 
    elif callback.data.split(":")[1] == "Fifty":
        case_id = callback.data.split(":")[0]
        await state.set_state(DCome.why)
        await state.update_data(why=case_id, type="Fifty")
        await callback.message.answer(_("Напишите пожалуйста причину", user.language))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id) 
    else:
        case_id = callback.data.split(":")[0]
        await state.set_state(DCome.why)
        await state.update_data(why=case_id, type="No")
        await callback.message.answer(_("Напишите пожалуйста причину", user.language))
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id) 


@router.message(DCome.why)
async def why_handler(message: Message, state: FSMContext, session: AsyncSession):
    user = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == int(message.from_user.id)))
    user = user.scalar()
    data = await state.get_data()
    case_id = data['why']

    if data['type'] == "Fifty":
        case = await session.execute(select(NewCase).options(selectinload(NewCase.people_fifty)).where(NewCase.case_id == int(case_id)))
        case = case.scalar()
        case.people_fifty.append(user)

    else:
        case = await session.execute(select(NewCase).options(selectinload(NewCase.people_rejected)).where(NewCase.case_id == int(case_id)))
        case = case.scalar()
        case.people_rejected.append(user)

    reason = MemberReason(
            reason_body=message.text,
            user_id = user.user_id,
            case_id = int(case_id)
    )
    session.add(reason)    
    session.add(case)
    await message.answer("Ок.")
    await session.commit()


# Обработчик для команды "/case" в личном чате администратора
@router.message(Command('case'), F.chat.type == 'private')
async def cmd_check_user_case(message: Message, state: FSMContext, session: AsyncSession):
    user = await session.execute(select(NewPeopleMembers).where(NewPeopleMembers.user_id == message.from_user.id))
    user = user.scalar()
    if user: 
        if user.is_admin:
            print(1)
            # Извлекаем номер дела из текста команды
            case_id = message.text.split()[1]
            # Получаем дело из базы данных с участниками, которые ответили "Да"
            case = await session.execute(select(NewCase).options(selectinload(NewCase.people_rejected)).where(NewCase.case_id == int(case_id)))
            case = case.scalar()
            casefif = await session.execute(select(NewCase).options(selectinload(NewCase.people_fifty)).where(NewCase.case_id == int(case_id)))
            casefif = casefif.scalar()
            if case:
                # Формируем сообщение с информацией о деле и участниках, которые ответили "Да"
                sps = f'Название дела: {case.name}\nКоличество участников: {case.people_count}\nТекст: {case.text}\nУчастники, ответившие "Нет":\n'
                
                for i in case.people_rejected:
                    reason = await session.execute(select(MemberReason).where(MemberReason.user_id == i.user_id and MemberReason.case_id == int(case_id)))
                    reason = reason.scalar()
                    sps += f'\n{i.user_id}-{i.name}-{i.phone_number}-Причина: {reason.reason_body}'

                sps += f'\nУчастники, ответившие "50/50":\n'
                
                for i in casefif.people_fifty:
                    reason = await session.execute(select(MemberReason).where(MemberReason.user_id == i.user_id and MemberReason.case_id == int(case_id)))
                    reason = reason.scalar()
                    sps += f'\n{i.user_id}-{i.name}-{i.phone_number}-Причина: {reason.reason_body}'

                with open(f"{case_id}.txt", "w", encoding="utf-16") as file:
                    file.write(sps)
                f = FSInputFile(f"{case_id}.txt")
                await message.answer_document(f)
                os.remove(f"{case_id}.txt")
            else:
                await message.answer("Такого кейса нет")