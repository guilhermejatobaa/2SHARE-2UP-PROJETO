from src.domain.money import Money
from src.domain.member import Member
from src.domain.exceptions import InvalidAmountError
from typing import List

class Expense:
    def __init__(self, expense_id: str, description: str, amount: Money, payer: Member, split_among: List[Member]):
        if amount.amount_cents <= 0:
            raise InvalidAmountError("O valor da despesa deve ser positivo.")
        if not split_among:
            raise InvalidAmountError("A despesa deve ser dividida com pelo menos uma pessoa.")

        self._id = expense_id
        self._description = description
        self._amount = amount
        self._payer = payer
        self._split_among = split_among

    @property
    def id(self) -> str:
        return self._id

    @property
    def amount(self) -> Money:
        return self._amount

    @property
    def payer(self) -> Member:
        return self._payer

    @property
    def split_among(self) -> List[Member]:
        return self._split_among
