import pytest
from core.bit_utils import zeros, int_to_array, array_to_int, invert, add_arrays, shift_left, shift_right


def test_zeros():
    assert zeros(5) == [0, 0, 0, 0, 0]


@pytest.mark.parametrize("val, bits, expected", [
    (5, 4, [0, 1, 0, 1]),
    (0, 3, [0, 0, 0]),
    (15, 4, [1, 1, 1, 1]),
])
def test_int_to_array(val, bits, expected):
    assert int_to_array(val, bits) == expected


@pytest.mark.parametrize("arr, expected", [
    ([0, 1, 0, 1], 5),
    ([0, 0, 0], 0),
    ([1, 1, 1, 1], 15),
])
def test_array_to_int(arr, expected):
    assert array_to_int(arr) == expected


def test_invert():
    assert invert([1, 0, 1, 0]) == [0, 1, 0, 1]


@pytest.mark.parametrize("arr_a, arr_b, expected_res, expected_carry", [
    ([0, 1, 0, 1], [0, 0, 1, 1], [1, 0, 0, 0], 0),
    ([1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0], 1),
])
def test_add_arrays(arr_a, arr_b, expected_res, expected_carry):
    assert add_arrays(arr_a, arr_b) == (expected_res, expected_carry)


@pytest.mark.parametrize("arr, steps, expected", [
    ([0, 1, 1, 0], 1, [1, 1, 0, 0]),
    ([0, 1, 1, 0], 2, [1, 0, 0, 0]),
    ([0, 1, 1, 0], 4, [0, 0, 0, 0]),
    ([0, 1, 1, 0], 0, [0, 1, 1, 0]),
])
def test_shift_left(arr, steps, expected):
    assert shift_left(arr, steps) == expected


@pytest.mark.parametrize("arr, steps, expected", [
    ([0, 1, 1, 0], 1, [0, 0, 1, 1]),
    ([0, 1, 1, 0], 2, [0, 0, 0, 1]),
    ([0, 1, 1, 0], 4, [0, 0, 0, 0]),
    ([0, 1, 1, 0], 0, [0, 1, 1, 0]),
])
def test_shift_right(arr, steps, expected):
    assert shift_right(arr, steps) == expected
