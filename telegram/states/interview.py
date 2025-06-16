from aiogram.fsm.state import State, StatesGroup


class InterviewStates(StatesGroup):
    waiting_for_answer = State()