from typing import List, Dict
from src.domain.group import Group, Settlement
from src.domain.member import Member
from src.domain.expense import Expense
from src.domain.money import Money


class GroupService:
    """
    Serviço de Aplicação responsável por orquestrar os Casos de Uso do sistema.
    Isola o Domínio de interações diretas com o mundo externo.
    """

    def __init__(self):
        # Armazenamento simples em memória para simular um repositório/banco de dados
        self._groups: Dict[str, Group] = {}

    def create_group(self, group_id: str, name: str) -> Group:
        group = Group(group_id, name)
        self._groups[group_id] = group
        return group

    def add_member_to_group(self, group_id: str, member_id: str, name: str) -> Member:
        if group_id not in self._groups:
            raise ValueError("Grupo não encontrado.")

        member = Member(member_id, name)
        self._groups[group_id].add_member(member)
        return member

    def register_group_expense(
            self,
            group_id: str,
            expense_id: str,
            description: str,
            amount_cents: int,
            payer_id: str,
            split_among_ids: List[str]
    ) -> None:
        if group_id not in self._groups:
            raise ValueError("Grupo não encontrado.")

        group = self._groups[group_id]

        # Recupera as referências das entidades baseado nos IDs enviados pela aplicação
        payer = group._members.get(payer_id)
        split_among = [group._members.get(m_id) for m_id in split_among_ids if group._members.get(m_id)]

        # Cria a despesa usando as regras e VOs do domínio
        expense = Expense(
            expense_id=expense_id,
            description=description,
            amount=Money(amount_cents),
            payer=payer,
            split_among=split_among
        )

        group.register_expense(expense)

    def process_clearing(self, group_id: str) -> List[Settlement]:
        if group_id not in self._groups:
            raise ValueError("Grupo não encontrado.")

        return self._groups[group_id].calculate_settlements()