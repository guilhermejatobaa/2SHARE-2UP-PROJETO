from src.domain.member import Member
from src.domain.expense import Expense
from src.domain.money import Money
from src.domain.exceptions import MemberNotFoundError
from typing import Dict, List
from dataclasses import dataclass


@dataclass(frozen=True)
class Settlement:
    """Value Object que representa uma instrução de pagamento para zerar dívidas."""
    payer: Member
    payee: Member
    amount: Money


class Group:
    """
    Aggregate Root (Raiz de Agregação).
    Garante a consistência das regras de negócio do grupo.
    """

    def __init__(self, group_id: str, name: str):
        self._id = group_id
        self._name = name
        self._members: Dict[str, Member] = {}
        self._expenses: List[Expense] = []

    def add_member(self, member: Member) -> None:
        self._members[member.id] = member

    def register_expense(self, expense: Expense) -> None:
        if expense.payer.id not in self._members:
            raise MemberNotFoundError("O pagador não faz parte deste grupo.")

        split_count = len(expense.split_among)
        split_amount_cents = expense.amount.amount_cents // split_count
        split_money = Money(split_amount_cents, expense.amount.currency)

        # O pagador recebe o crédito integral
        self._members[expense.payer.id].add_funds(expense.amount)

        # Debita a parte de cada um envolvido no rateio
        for member in expense.split_among:
            if member.id not in self._members:
                raise ValueError(f"O membro {member.name} não faz parte deste grupo.")

            self._members[member.id].deduct_funds(split_money)

        self._expenses.append(expense)

    def calculate_settlements(self) -> List[Settlement]:
        """Algoritmo Greedy para minimizar as transferências financeiras."""
        balances = {
            member: member.balance.amount_cents
            for member in self._members.values()
            if member.balance.amount_cents != 0
        }

        debtors = sorted([m for m, bal in balances.items() if bal < 0], key=lambda m: balances[m])
        creditors = sorted([m for m, bal in balances.items() if bal > 0], key=lambda m: balances[m], reverse=True)

        settlements = []
        i, j = 0, 0

        while i < len(debtors) and j < len(creditors):
            debtor = debtors[i]
            creditor = creditors[j]

            debt = -balances[debtor]
            credit = balances[creditor]

            settled_amount = min(debt, credit)

            settlements.append(Settlement(payer=debtor, payee=creditor, amount=Money(settled_amount)))

            balances[debtor] += settled_amount
            balances[creditor] -= settled_amount

            if balances[debtor] == 0:
                i += 1
            if balances[creditor] == 0:
                j += 1

        return settlements