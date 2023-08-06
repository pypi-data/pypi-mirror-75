from enum import Enum


class TRANSACTION_TYPES(Enum):
    Deposit = "Deposit"
    Trade = "Trade"
    Withdrawal = "Withdrawal"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
