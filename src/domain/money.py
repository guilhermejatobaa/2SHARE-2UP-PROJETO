from dataclasses import dataclass
from src.domain.exceptions import CurrencyMismatchError

@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str = "BRL"

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise CurrencyMismatchError("Não é possível somar moedas diferentes.")
        return Money(self.amount_cents + other.amount_cents, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise CurrencyMismatchError("Não é possível subtrair moedas diferentes.")
        return Money(self.amount_cents - other.amount_cents, self.currency)