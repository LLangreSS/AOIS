import pytest
from core.gray_bcd import bin_to_gray_tetrad, gray_to_bin_tetrad, to_gray_bcd, array_to_decimal, add
from core.constants import WORD_SIZE


@pytest.mark.parametrize("bin_arr, expected_gray", [
    ([0, 0, 0, 0], [0, 0, 0, 0]),
    ([0, 0, 0, 1], [0, 0, 0, 1]),
    ([0, 0, 1, 0], [0, 0, 1, 1]),
    ([0, 1, 0, 1], [0, 1, 1, 1]),
    ([1, 0, 0, 1], [1, 1, 0, 1]),
])
def test_bin_to_gray_tetrad(bin_arr, expected_gray):
    assert bin_to_gray_tetrad(bin_arr) == expected_gray


@pytest.mark.parametrize("gray_arr, expected_bin", [
    ([0, 0, 0, 0], [0, 0, 0, 0]),
    ([0, 0, 0, 1], [0, 0, 0, 1]),
    ([0, 0, 1, 1], [0, 0, 1, 0]),
    ([0, 1, 1, 1], [0, 1, 0, 1]),
    ([1, 1, 0, 1], [1, 0, 0, 1]),
])
def test_gray_to_bin_tetrad(gray_arr, expected_bin):
    assert gray_to_bin_tetrad(gray_arr) == expected_bin


def test_to_gray_bcd_and_back():
    val = 125
    arr = to_gray_bcd(val)
    assert len(arr) == WORD_SIZE
    assert array_to_decimal(arr) == val


@pytest.mark.parametrize("val1, val2, expected", [
    (15, 22, 37),
    (9, 9, 18),
    (99, 1, 100),
    (123, 456, 579),
])
def test_add(val1, val2, expected):
    _, dec_val = add(val1, val2)
    assert dec_val == expected
