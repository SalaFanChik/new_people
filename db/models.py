from sqlalchemy import Column, BIGINT, Boolean, String, Integer, Text, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from typing import List

from db.base import Base

# Определение таблицы связи между делами и участниками (многие ко многим)
association_table = Table(
    "association_table",
    Base.metadata,
    Column("Case_id", ForeignKey("Case.case_id"), primary_key=True),  # Внешний ключ к таблице дел
    Column("NP_members_id", ForeignKey("NP_members.user_id"), primary_key=True),  # Внешний ключ к таблице участников
    extend_existing=True
)


association_table2 = Table(
    "association_table2",
    Base.metadata,
    Column("Case_id", ForeignKey("Case.case_id"), primary_key=True),  # Внешний ключ к таблице дел
    Column("NP_members_id", ForeignKey("NP_members.user_id"), primary_key=True),  # Внешний ключ к таблице участников
    extend_existing=True
)

association_table3 = Table(
    "association_table3",
    Base.metadata,
    Column("Case_id", ForeignKey("Case.case_id"), primary_key=True),  # Внешний ключ к таблице дел
    Column("NP_members_id", ForeignKey("NP_members.user_id"), primary_key=True),  # Внешний ключ к таблице участников
    extend_existing=True
)

class MemberReason(Base):
    __tablename__ = "Reason"

    reason_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)  
    reason_body = Column(Text, unique=False) 
    user_id: Mapped[BIGINT] = mapped_column(ForeignKey("NP_members.user_id"))
    case_id: Mapped[int] = mapped_column(ForeignKey("Case.case_id")) 

class NewCase(Base):
    __tablename__ = "Case"

    case_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)  # Уникальный идентификатор дела
    name = Column(String, unique=True)  # Название дела
    people_count = Column(Integer, unique=False)  # Количество участников дела
    people_accepted: Mapped[List["NewPeopleMembers"]] = relationship(
        secondary=association_table, back_populates="case",  # Связь многие ко многим с таблицей участников
    )
    people_rejected: Mapped[List["NewPeopleMembers"]] = relationship(
        secondary=association_table2, back_populates="case_rejected",  # Связь многие ко многим с таблицей участников
    )
    people_fifty: Mapped[List["NewPeopleMembers"]] = relationship(
        secondary=association_table3, back_populates="case_fifty",  # Связь многие ко многим с таблицей участников
    )
    image = Column(String)  # Путь к изображению (если есть)
    text = Column(String)  # Текстовое описание дела



class NewPeopleMembers(Base):
    __tablename__ = "NP_members"

    user_id = Column(BIGINT, primary_key=True, unique=True, autoincrement=False)  # Уникальный идентификатор участника
    is_admin = Column(Boolean, unique=False, default=False)  # Флаг, указывающий, является ли участник администратором
    name = Column(String, unique=False)  # Имя участника
    case: Mapped[List["NewCase"]] = relationship(
        secondary=association_table, back_populates="people_accepted",  # Связь многие ко многим с таблицей дел
    )
    case_rejected: Mapped[List["NewCase"]] = relationship(
        secondary=association_table2, back_populates="people_rejected",  # Связь многие ко многим с таблицей дел
    )
    case_fifty: Mapped[List["NewCase"]] = relationship(
        secondary=association_table3, back_populates="people_fifty",  # Связь многие ко многим с таблицей дел
    )
    phone_number = Column(BIGINT, unique=False)  # Номер телефона участника
    th_text = Column(Text, unique=False)  # Текстовое мнение пользователя о проекте
    sg_text = Column(Text, unique=False)  # Предложения пользователя по улучшению проекта
    language = Column(String, unique=False)


class NewPeopleChats(Base):
    __tablename__ = "NP_chats"
    chat_id = Column(BIGINT, primary_key=True, unique=True, autoincrement=False)  # Уникальный идентификатор чата
    # Дополнительные поля чата, ко00торые вы хотите сохранить (вам нужно добавить их сюда)

# Примечание: Каждый класс представляет собой отдельную таблицу в базе данных.
# Связи между таблицами устанавливаются с использованием внешних ключей и отношений.
