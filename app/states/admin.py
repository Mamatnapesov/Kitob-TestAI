from aiogram.fsm.state import State, StatesGroup


class AddBookState(StatesGroup):
    name = State()
    author = State()
    description = State()
    cover = State()


class AddTestState(StatesGroup):
    book = State()
    question = State()
    option_a = State()
    option_b = State()
    option_c = State()
    option_d = State()
    correct = State()
    difficulty = State()


class ImportTestState(StatesGroup):
    book = State()
    file = State()