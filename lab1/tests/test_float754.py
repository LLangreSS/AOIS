import pytest
from core.float754 import parse_to_array, array_to_float_str, add, multiply, divide, _pack
from core.constants import WORD_SIZE, MANTISSA_BITS


def test_pack_out_of_bounds():
    assert _pack(0, 0, [0] * MANTISSA_BITS) == [0] * WORD_SIZE
    assert _pack(0, 255, [0] * MANTISSA_BITS) == [0] * WORD_SIZE


@pytest.mark.parametrize("value_str", [
    "0.0", "-0.0", "1.0", "-1.0", "0.5", "1.5", "0.125", "10.25", "0", "-5"
])
def test_parse_and_to_str(value_str):
    arr = parse_to_array(value_str)
    if float(value_str) == 0.0:
        assert array_to_float_str(arr) == "0.0"
    else:
        assert array_to_float_str(arr) == str(float(value_str))


@pytest.mark.parametrize("val1, val2, expected", [
    ("1.0", "1.0", "2.0"),
    ("1.5", "1.5", "3.0"),
    ("-1.5", "-1.5", "-3.0"),
    ("0.0", "5.0", "5.0"),
    ("5.0", "0.0", "5.0"),
    ("0.0", "0.0", "0.0"),
    ("2.5", "-1.25", "1.25"),
    ("-2.5", "1.25", "-1.25"),
    ("1.25", "-2.5", "-1.25"),
    ("1.0", "-1.0", "0.0"),
    ("-1.0", "1.0", "0.0"),
    ("1.5", "-1.25", "0.25"),
])
def test_add_full(val1, val2, expected):
    arr_a = parse_to_array(val1)
    arr_b = parse_to_array(val2)
    res_arr = add(arr_a, arr_b)
    assert array_to_float_str(res_arr) == expected


@pytest.mark.parametrize("val1, val2, expected", [
    ("0.0", "5.0", "0.0"),
    ("5.0", "0.0", "0.0"),
    ("1.5", "1.5", "2.25"),
    ("2.0", "3.0", "6.0"),
    ("1.0", "1.25", "1.25"),
    ("-2.0", "1.5", "-3.0"),
])
def test_multiply_full(val1, val2, expected):
    arr_a = parse_to_array(val1)
    arr_b = parse_to_array(val2)
    res_arr = multiply(arr_a, arr_b)
    assert array_to_float_str(res_arr) == expected


@pytest.mark.parametrize("val1, val2, expected", [
    ("0.0", "5.0", "0.0"),
    ("1.0", "2.0", "0.5"),
    ("1.0", "1.25", "0.7999999523162842"),
    ("3.0", "1.5", "2.0"),
    ("-3.0", "1.5", "-2.0"),
])
def test_divide_full(val1, val2, expected):
    arr_a = parse_to_array(val1)
    arr_b = parse_to_array(val2)
    res_arr = divide(arr_a, arr_b)
    assert array_to_float_str(res_arr) == expected


def test_divide_by_zero():
    arr_a = parse_to_array("1.0")
    arr_zero = parse_to_array("0.0")
    with pytest.raises(ValueError, match="Division by zero"):
        divide(arr_a, arr_zero)


def test_divide_underflow():
    arr_a = _pack(0, 10, [0] * MANTISSA_BITS)
    arr_b = _pack(0, 200, [0] * MANTISSA_BITS)
    assert divide(arr_a, arr_b) == [0] * WORD_SIZE


def test_large_number_to_str():
    arr = parse_to_array("16777216.0")
    assert array_to_float_str(arr) == "16777216.0"
