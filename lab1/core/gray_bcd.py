from core.logic_gates import logic_xor, logic_or
from core.bit_utils import BitArray, int_to_array, array_to_int, add_arrays, zeros
from core.constants import WORD_SIZE, TETRAD_SIZE


def bin_to_gray_tetrad(b: BitArray) -> BitArray:
    g = zeros(TETRAD_SIZE)
    g[0] = b[0]
    g[1] = logic_xor(b[0], b[1])
    g[2] = logic_xor(b[1], b[2])
    g[3] = logic_xor(b[2], b[3])
    return g


def gray_to_bin_tetrad(g: BitArray) -> BitArray:
    b = zeros(TETRAD_SIZE)
    b[0] = g[0]
    b[1] = logic_xor(b[0], g[1])
    b[2] = logic_xor(b[1], g[2])
    b[3] = logic_xor(b[2], g[3])
    return b


def to_gray_bcd(n: int) -> BitArray:
    arr = zeros(WORD_SIZE)
    val_str = str(abs(n))

    while len(val_str) < (WORD_SIZE // TETRAD_SIZE):
        val_str = "0" + val_str

    for i, char in enumerate(val_str):
        digit = int(char)
        bin_tetrad = int_to_array(digit, TETRAD_SIZE)
        gray_tetrad = bin_to_gray_tetrad(bin_tetrad)
        arr[i * TETRAD_SIZE: i * TETRAD_SIZE + TETRAD_SIZE] = gray_tetrad
    return arr


def array_to_decimal(arr: BitArray) -> int:
    val_str = ""
    for i in range(0, WORD_SIZE, TETRAD_SIZE):
        gray_tetrad = arr[i:i + TETRAD_SIZE]
        bin_tetrad = gray_to_bin_tetrad(gray_tetrad)
        digit = array_to_int(bin_tetrad)
        val_str += str(digit)
    return int(val_str)


def add(a: int, b: int) -> tuple[BitArray, int]:
    arr_a = to_gray_bcd(a)
    arr_b = to_gray_bcd(b)
    res_arr = zeros(WORD_SIZE)
    carry = 0

    for i in range((WORD_SIZE // TETRAD_SIZE) - 1, -1, -1):
        idx = i * TETRAD_SIZE
        tetrad_a_gray = arr_a[idx:idx + TETRAD_SIZE]
        tetrad_b_gray = arr_b[idx:idx + TETRAD_SIZE]

        tetrad_a_bin = gray_to_bin_tetrad(tetrad_a_gray)
        tetrad_b_bin = gray_to_bin_tetrad(tetrad_b_gray)

        sum_bin, carry_out1 = add_arrays(tetrad_a_bin, tetrad_b_bin)
        carry_arr = int_to_array(carry, TETRAD_SIZE)
        sum_bin, carry_out2 = add_arrays(sum_bin, carry_arr)

        tetrad_carry = logic_or(carry_out1, carry_out2)
        sum_val = array_to_int(sum_bin)

        if sum_val > 9 or tetrad_carry == 1:
            correction = int_to_array(6, TETRAD_SIZE)
            sum_bin, _ = add_arrays(sum_bin, correction)
            carry = 1
        else:
            carry = 0

        sum_bin = sum_bin[-TETRAD_SIZE:]
        res_tetrad_gray = bin_to_gray_tetrad(sum_bin)
        res_arr[idx:idx + TETRAD_SIZE] = res_tetrad_gray

    return res_arr, array_to_decimal(res_arr)
