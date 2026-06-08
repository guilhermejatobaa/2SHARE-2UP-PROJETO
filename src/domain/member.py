from src.domain.money import Money

class Member:
    def __init__(self, member_id: str, name: str):
        self._id = member_id
        self._name = name
        self._balance = Money(0)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def balance(self) -> Money:
        return self._balance

    def add_funds(self, amount: Money) -> None:
        # Atribuição explícita garante que o novo Value Object seja salvo corretamente
        self._balance = self._balance + amount

    def deduct_funds(self, amount: Money) -> None:
        # Atribuição explícita garante que o novo Value Object seja salvo corretamente
        self._balance = self._balance - amount