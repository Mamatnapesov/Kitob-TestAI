from aiogram.filters.callback_data import CallbackData


# =========================
# BOOK CALLBACKS
# =========================

class EditBookCallback(CallbackData, prefix="edit_book"):
    id: int


class DeleteBookCallback(CallbackData, prefix="delete_book"):
    id: int


# =========================
# TEST CALLBACKS
# =========================

class EditTestCallback(CallbackData, prefix="edit_test"):
    id: int


class DeleteTestCallback(CallbackData, prefix="delete_test"):
    id: int


# =========================
# USER CALLBACKS
# =========================

class UserCallback(CallbackData, prefix="user"):
    action: str
    id: int


# =========================
# STATISTICS CALLBACKS
# =========================

class StatisticsCallback(CallbackData, prefix="statistics"):
    action: str


# =========================
# BROADCAST CALLBACKS
# =========================

class BroadcastCallback(CallbackData, prefix="broadcast"):
    action: str