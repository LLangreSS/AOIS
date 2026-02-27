from core.logic_gates import logic_not, full_adder
from core.constants import WORD_SIZE

BitArray = list[int]


def zeros(size: int) -> BitArray:
    return [0] * size


def int_to_array(n: int, bits: int = WORD_SIZE) -> BitArray:
    arr = zeros(bits)
    val = abs(n)
    for i in range(bits - 1, -1, -1):
        arr[i] = val % 2
        val = val // 2
    return arr


def array_to_int(arr: BitArray) -> int:
    val = 0
    for bit in arr:
        val = val * 2 + bit
    return val


def invert(arr: BitArray) -> BitArray:
    return [logic_not(b) for b in arr]


def add_arrays(a: BitArray, b: BitArray) -> tuple[BitArray, int]:
    res = zeros(len(a))
    carry = 0
    for i in range(len(a) - 1, -1, -1):
        sum_bit, carry = full_adder(a[i], b[i], carry)
        res[i] = sum_bit
    return res, carry


def shift_left(arr: BitArray, steps: int) -> BitArray:
    if steps == 0:
        return arr
    if steps >= len(arr):
        return zeros(len(arr))
    return arr[steps:] + zeros(steps)


def shift_right(arr: BitArray, steps: int) -> BitArray:
    if steps == 0:
        return arr
    if steps >= len(arr):
        return zeros(len(arr))
    return zeros(steps) + arr[:-steps]
