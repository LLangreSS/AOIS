from core.logic_gates import logic_not, logic_xor
from core.bit_utils import BitArray, int_to_array, array_to_int, add_arrays, shift_left, zeros
from core.constants import WORD_SIZE


def to_direct_code(n: int) -> BitArray:
    arr = int_to_array(n, WORD_SIZE)
    if n < 0:
        arr[0] = 1
    return arr


def to_ones_complement(n: int) -> BitArray:
    arr = to_direct_code(n)
    if n < 0:
        for i in range(1, WORD_SIZE):
            arr[i] = logic_not(arr[i])
    return arr


def to_twos_complement(n: int) -> BitArray:
    arr = to_ones_complement(n)
    if n < 0:
        one = int_to_array(1, WORD_SIZE)
        arr, _ = add_arrays(arr, one)
    return arr


def twos_comp_to_decimal(arr: BitArray) -> int:
    if arr[0] == 0:
        return array_to_int(arr)
    inverted = [logic_not(b) for b in arr]
    one = int_to_array(1, WORD_SIZE)
    abs_arr, _ = add_arrays(inverted, one)
    return -array_to_int(abs_arr)


def add(a: int, b: int) -> tuple[BitArray, int]:
    arr_a = to_twos_complement(a)
    arr_b = to_twos_complement(b)
    res_arr, _ = add_arrays(arr_a, arr_b)
    return res_arr, twos_comp_to_decimal(res_arr)


def difference(a: int, b: int) -> tuple[BitArray, int]:
    return add(a, -b)


def multiply(a: int, b: int) -> tuple[BitArray, int]:
    arr_a = to_direct_code(a)
    arr_b = to_direct_code(b)
    sign = logic_xor(arr_a[0], arr_b[0])
    res = zeros(WORD_SIZE)

    for i in range(WORD_SIZE - 1, 0, -1):
        if arr_b[i] == 1:
            shift_amount = (WORD_SIZE - 1) - i
            shifted_a = shift_left(arr_a, shift_amount)
            shifted_a[0] = 0
            res, _ = add_arrays(res, shifted_a)

    res[0] = sign
    dec_val = array_to_int(res[1:])
    if sign == 1:
        dec_val = -dec_val

    return res, dec_val


def divide(a: int, b: int) -> tuple[BitArray, BitArray, str]:
    if b == 0:
        raise ValueError("Division by zero")

    sign_bit = 1 if (a < 0) != (b < 0) else 0
    a_val = abs(a)
    b_val = abs(b)

    int_val = a_val // b_val
    int_arr = int_to_array(int_val, WORD_SIZE)
    int_arr[0] = sign_bit

    frac_arr = zeros(5)
    temp_rem = a_val % b_val

    for i in range(5):
        temp_rem *= 2
        if temp_rem >= b_val:
            frac_arr[i] = 1
            temp_rem -= b_val
        else:
            frac_arr[i] = 0

    rem = a_val % b_val
    frac_dec = (rem * 100000) // b_val
    sign_char = "-" if sign_bit else ""
    dec_str = f"{sign_char}{int_val}.{frac_dec:05d}"

    return int_arr, frac_arr, dec_str
