from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class ExamState(StatesGroup):

    solving = State()