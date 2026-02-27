import pytest
from core.logic_gates import logic_and, logic_or, logic_xor, logic_not, full_adder


@pytest.mark.parametrize("a, b, expected", [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
])
def test_logic_and(a, b, expected):
    assert logic_and(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
])
def test_logic_or(a, b, expected):
    assert logic_or(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 0),
])
def test_logic_xor(a, b, expected):
    assert logic_xor(a, b) == expected


@pytest.mark.parametrize("a, expected", [
    (0, 1),
    (1, 0),
])
def test_logic_not(a, expected):
    assert logic_not(a) == expected


@pytest.mark.parametrize("a, b, carry_in, expected_sum, expected_carry", [
    (0, 0, 0, 0, 0),
    (1, 0, 0, 1, 0),
    (0, 1, 0, 1, 0),
    (1, 1, 0, 0, 1),
    (0, 0, 1, 1, 0),
    (1, 0, 1, 0, 1),
    (0, 1, 1, 0, 1),
    (1, 1, 1, 1, 1),
])
def test_full_adder(a, b, carry_in, expected_sum, expected_carry):
    assert full_adder(a, b, carry_in) == (expected_sum, expected_carry)
