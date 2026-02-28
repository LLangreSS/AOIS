from core.logic_gates import logic_xor
from core.bit_utils import BitArray, int_to_array, array_to_int, add_arrays, shift_left, shift_right, zeros
from core.constants import WORD_SIZE, MANTISSA_BITS, EXPONENT_BITS, EXPONENT_BIAS


def _is_zero(arr: BitArray) -> bool:
    return all(b == 0 for b in arr[1:])


def _unpack(arr: BitArray) -> tuple[int, int, BitArray]:
    sign = arr[0]
    exp = array_to_int(arr[1:1 + EXPONENT_BITS])
    mantissa_arr = [1] + arr[1 + EXPONENT_BITS:]
    return sign, exp, mantissa_arr


def _pack(sign: int, exp: int, mantissa: BitArray) -> BitArray:
    if exp <= 0 or exp >= (2 ** EXPONENT_BITS - 1):
        return zeros(WORD_SIZE)
    exp_arr = int_to_array(exp, EXPONENT_BITS)
    return [sign] + exp_arr + mantissa


def _align_exponents(exp_a: int, mantis_a: BitArray, exp_b: int, mantis_b: BitArray) -> tuple[int, BitArray, BitArray]:
    if exp_a > exp_b:
        return exp_a, mantis_a, shift_right(mantis_b, exp_a - exp_b)
    return exp_b, shift_right(mantis_a, exp_b - exp_a), mantis_b


def parse_to_array(num_str: str) -> BitArray:
    sign_bit = 1 if num_str.startswith('-') else 0
    num_str = num_str.lstrip('-')
    parts = num_str.split('.')
    int_part = int(parts[0]) if parts[0] else 0
    frac_str = parts[1] if len(parts) > 1 else "0"

    int_bits = []
    temp = int_part
    while temp > 0:
        int_bits.insert(0, temp % 2)
        temp = temp // 2

    frac_bits = []
    frac_val = int(frac_str)
    denom = 10 ** len(frac_str)

    for _ in range(WORD_SIZE):
        frac_val *= 2
        if frac_val >= denom:
            frac_bits.append(1)
            frac_val -= denom
        else:
            frac_bits.append(0)

    if int_part == 0 and all(b == 0 for b in frac_bits):
        return zeros(WORD_SIZE)

    if int_part > 0:
        exp = EXPONENT_BIAS + len(int_bits) - 1
        mantissa = int_bits[1:] + frac_bits
    else:
        first_one_idx = frac_bits.index(1)
        exp = EXPONENT_BIAS - (first_one_idx + 1)
        mantissa = frac_bits[first_one_idx + 1:]

    mantissa_arr = (mantissa + zeros(MANTISSA_BITS))[:MANTISSA_BITS]
    return _pack(sign_bit, exp, mantissa_arr)


def array_to_float_str(arr: BitArray) -> str:
    if _is_zero(arr):
        return "0.0"

    sign = "-" if arr[0] == 1 else ""
    exp = array_to_int(arr[1:1 + EXPONENT_BITS]) - EXPONENT_BIAS
    mantissa_bits = arr[1 + EXPONENT_BITS:]
    mantissa_int = (2 ** MANTISSA_BITS) + array_to_int(mantissa_bits)

    if exp >= MANTISSA_BITS:
        val = mantissa_int * (2 ** (exp - MANTISSA_BITS))
        return f"{sign}{val}.0"

    val = mantissa_int / (2 ** (MANTISSA_BITS - exp))
    return f"{sign}{val}"


def add(arr_a: BitArray, arr_b: BitArray) -> BitArray:
    if _is_zero(arr_a):
        return arr_b

    if _is_zero(arr_b):
        return arr_a

    sign_a, exp_a, mantis_a = _unpack(arr_a)
    sign_b, exp_b, mantis_b = _unpack(arr_b)

    exp_res, mantis_a, mantis_b = _align_exponents(exp_a, mantis_a, exp_b, mantis_b)

    if sign_a == sign_b:
        res_mantis, carry = add_arrays(mantis_a, mantis_b)
        sign_res = sign_a
        if carry:
            res_mantis = [carry] + res_mantis[:-1]
            exp_res += 1
        res_mantis_23 = res_mantis[1:MANTISSA_BITS + 1]
    else:
        val_a, val_b = array_to_int(mantis_a), array_to_int(mantis_b)
        sign_res = sign_a if val_a >= val_b else sign_b
        diff_val = abs(val_a - val_b)

        if diff_val == 0:
            return zeros(WORD_SIZE)

        res_mantis = int_to_array(diff_val, MANTISSA_BITS + 1)
        shift = 0
        while shift < MANTISSA_BITS + 1 and res_mantis[shift] == 0:
            shift += 1
        res_mantis = res_mantis[shift:] + zeros(shift)
        exp_res -= shift
        res_mantis_23 = res_mantis[1:MANTISSA_BITS + 1]

    return _pack(sign_res, exp_res, res_mantis_23)


def subtract(arr_a: BitArray, arr_b: BitArray) -> BitArray:
    if _is_zero(arr_b):
        return arr_a

    neg_b = list(arr_b)

    neg_b[0] = 1 - neg_b[0]

    return add(arr_a, neg_b)


def multiply(arr_a: BitArray, arr_b: BitArray) -> BitArray:
    if _is_zero(arr_a) or _is_zero(arr_b):
        return zeros(WORD_SIZE)

    sign_a, exp_a, mantis_a_arr = _unpack(arr_a)
    sign_b, exp_b, mantis_b_arr = _unpack(arr_b)

    sign_res = logic_xor(sign_a, sign_b)
    exp_res = exp_a + exp_b - EXPONENT_BIAS

    mantis_a = array_to_int(mantis_a_arr)
    mantis_b = array_to_int(mantis_b_arr)
    mantis_res_arr = int_to_array(mantis_a * mantis_b, (MANTISSA_BITS + 1) * 2)

    if mantis_res_arr[0] == 1:
        exp_res += 1
        final_mantissa = mantis_res_arr[1:MANTISSA_BITS + 1]
    else:
        final_mantissa = mantis_res_arr[2:MANTISSA_BITS + 2]

    return _pack(sign_res, exp_res, final_mantissa)


def divide(arr_a: BitArray, arr_b: BitArray) -> BitArray:
    if _is_zero(arr_b):
        raise ValueError("Division by zero")
    if _is_zero(arr_a):
        return zeros(WORD_SIZE)

    sign_a, exp_a, mantis_a_arr = _unpack(arr_a)
    sign_b, exp_b, mantis_b_arr = _unpack(arr_b)

    sign_res = logic_xor(sign_a, sign_b)
    exp_res = exp_a - exp_b + EXPONENT_BIAS

    mantis_a_shifted_arr = mantis_a_arr + zeros(MANTISSA_BITS)
    val_a_shifted = array_to_int(mantis_a_shifted_arr)
    val_b = array_to_int(mantis_b_arr)

    val_res = val_a_shifted // val_b

    if val_res < (2 ** MANTISSA_BITS):
        val_res_arr = int_to_array(val_res, (MANTISSA_BITS + 1) * 2)
        val_res_shifted = shift_left(val_res_arr, 1)
        val_res = array_to_int(val_res_shifted)
        exp_res -= 1

    if exp_res <= 0:
        return zeros(WORD_SIZE)

    res_mantis_23 = int_to_array(val_res, MANTISSA_BITS + 1)[1:]
    return _pack(sign_res, exp_res, res_mantis_23)
