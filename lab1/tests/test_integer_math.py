import pytest
from core.integer_math import to_direct_code, to_ones_complement, to_twos_complement, twos_comp_to_decimal, add, \
    difference, multiply, divide
from core.constants import WORD_SIZE


@pytest.mark.parametrize("val, expected_sign", [
    (5, 0),
    (-5, 1),
    (0, 0),
])
def test_to_direct_code(val, expected_sign):
    arr = to_direct_code(val)
    assert len(arr) == WORD_SIZE
    assert arr[0] == expected_sign


def test_twos_complement_conversion():
    val = -42
    arr = to_twos_complement(val)
    assert twos_comp_to_decimal(arr) == val

    val_pos = 42
    arr_pos = to_twos_complement(val_pos)
    assert twos_comp_to_decimal(arr_pos) == val_pos


@pytest.mark.parametrize("val1, val2, expected", [
    (10, 5, 15),
    (-10, 5, -5),
    (-5, -5, -10),
    (20, -25, -5),
])
def test_add(val1, val2, expected):
    _, dec_val = add(val1, val2)
    assert dec_val == expected


@pytest.mark.parametrize("val1, val2, expected", [
    (10, 5, 5),
    (-10, 5, -15),
    (5, -5, 10),
    (-5, -5, 0),
])
def test_difference(val1, val2, expected):
    _, dec_val = difference(val1, val2)
    assert dec_val == expected


@pytest.mark.parametrize("val1, val2, expected", [
    (10, 5, 50),
    (-10, 5, -50),
    (-5, -5, 25),
    (0, 5, 0),
])
def test_multiply(val1, val2, expected):
    _, dec_val = multiply(val1, val2)
    assert dec_val == expected


@pytest.mark.parametrize("val1, val2, expected_str", [
    (10, 2, "5.00000"),
    (10, 3, "3.33333"),
    (-10, 4, "-2.50000"),
    (-10, -5, "2.00000"),
])
def test_divide(val1, val2, expected_str):
    _, _, dec_str = divide(val1, val2)
    assert dec_str == expected_str


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero"):
        divide(10, 0)
