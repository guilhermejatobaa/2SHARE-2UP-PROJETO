from src.domain.member import Member
from src.domain.expense import Expense
from src.domain.money import Money
from typing import Dict, List

class Group:
    def __init__(self, group_id: str, name: str):
        self._id = group_id
        self._name = name
        self._members: Dict[str, Member] = {}
        self._expenses: List[Expense] = []

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    def register_expense(self, expense: Expense) -> None:
        if expense.payer.id not in self._members:
            raise ValueError("O pagador não faz parte deste grupo.")

        split_count = len(expense.split_among)
        split_amount_cents = expense.amount.amount_cents // split_count
        split_money = Money(split_amount_cents, expense.amount.currency)

        self._members[expense.payer.id].add_funds(expense.amount)

        for member in expense.split_among:
            if member.id not in self._members:
                raise ValueError(f"O membro {member.name} não faz parte deste grupo.")
            self._members[member.id].deduct_funds(split_money)

        self._expenses.append(expense)
