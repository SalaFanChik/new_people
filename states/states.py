from aiogram.fsm.state import State, StatesGroup

class DCome(StatesGroup):
    why = State()
    type = State()

    
class PollState(StatesGroup):
    language = State()
    name = State()
    phone_number = State()
    th_text = State()
    sg_text = State()
    #нужно добавить переменные если хотите добавить новые вопросы, переменные должны быть названны правильно 

class CaseState(StatesGroup):
    to_who = State()
    name = State()
    text = State()

