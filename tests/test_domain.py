import pytest
from src.domain.money import Money
from src.domain.member import Member
from src.domain.expense import Expense
from src.domain.group import Group

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
