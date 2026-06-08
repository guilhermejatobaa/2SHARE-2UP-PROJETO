import pytest
from src.domain.money import Money
from src.domain.member import Member
from src.domain.expense import Expense
from src.domain.group import Group
from src.domain.group import Settlement

def test_money_immutability_and_equality():
    m1 = Money(1000) # R$ 10,00
    m2 = Money(1000)
    m3 = Money(500)

    assert m1 == m2
    assert m1 != m3

    with pytest.raises(ValueError):
        m1 + Money(1000, "USD")

def test_member_balance_encapsulation():
    member = Member("1", "Guilherme")
    assert member.balance == Money(0)

    member.add_funds(Money(5000))
    assert member.balance == Money(5000)

def test_group_expense_split():
    group = Group("g1", "Viagem Praia")

    m1 = Member("1", "Guilherme")
    m2 = Member("2", "João")
    m3 = Member("3", "Maria")

    group.add_member(m1)
    group.add_member(m2)
    group.add_member(m3)

    cost = Money(9000)
    expense = Expense("e1", "Aluguel Carro", cost, payer=m1, split_among=[m1, m2, m3])

    group.register_expense(expense)

    assert m1.balance == Money(6000)
    assert m2.balance == Money(-3000)
    assert m3.balance == Money(-3000)


def test_group_clearing_algorithm():
    group = Group("g2", "Churrasco")

    m1 = Member("1", "Guilherme")
    m2 = Member("2", "João")
    m3 = Member("3", "Maria")

    group.add_member(m1)
    group.add_member(m2)
    group.add_member(m3)

    # Guilherme pagou a carne: R$ 90,00 para os 3
    group.register_expense(Expense("e1", "Carne", Money(9000), payer=m1, split_among=[m1, m2, m3]))

    # João pagou a bebida: R$ 30,00 para os 3
    group.register_expense(Expense("e2", "Bebida", Money(3000), payer=m2, split_among=[m1, m2, m3]))

    # Saldos internos esperados:
    # Guilherme gastou 90, mas consumiu 40 (30 da carne + 10 da bebida). Saldo: +50
    # João gastou 30, mas consumiu 40. Saldo: -10
    # Maria não gastou nada, consumiu 40. Saldo: -40

    settlements = group.calculate_settlements()

    assert len(settlements) == 2

    # Maria deve 40 para Guilherme
    assert any(s.payer.name == "Maria" and s.payee.name == "Guilherme" and s.amount == Money(4000) for s in settlements)
    # João deve 10 para Guilherme
    assert any(s.payer.name == "João" and s.payee.name == "Guilherme" and s.amount == Money(1000) for s in settlements)