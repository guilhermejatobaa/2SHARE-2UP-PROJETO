class DomainError(Exception):
    """Classe base para todas as exceções de negócio."""
    pass

class CurrencyMismatchError(DomainError):
    """Lançada quando tentamos operar com moedas diferentes."""
    pass

class InvalidAmountError(DomainError):
    """Lançada quando o valor financeiro é inválido para a operação."""
    pass

class MemberNotFoundError(DomainError):
    """Lançada quando um membro não pertence ao grupo ou não foi encontrado."""
    pass