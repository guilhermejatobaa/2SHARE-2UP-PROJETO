from src.domain.group import Group, Settlement
from src.domain.member import Member
from src.domain.expense import Expense
from src.domain.money import Money
from typing import List

class GroupService:
    """
    Serviço de Aplicação que orquestra as ações do usuário.
    É aqui que a interface (web/desktop) se conectaria.
    """
    def __init__(self, group: Group):
        self.group = group

    def add_member_to_group(self, member_id: str, name: str) -> None:
        member = Member(member_id, name)
        self.group.add_member(member)

    def add_expense(self, expense_id: str, desc: str, cents: int, payer: Member, split_with: List[Member]) -> None:
        expense = Expense(expense_id, desc, Money(cents), payer, split_with)
        self.group.register_expense(expense)

    def settle_debts(self) -> List[Settlement]:
        return self.group.calculate_settlements()