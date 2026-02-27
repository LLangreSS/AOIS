def logic_and(a: int, b: int) -> int:
    return a * b


def logic_or(a: int, b: int) -> int:
    return 1 if (a + b) > 0 else 0


def logic_xor(a: int, b: int) -> int:
    return 1 if a != b else 0


def logic_not(a: int) -> int:
    return 1 - a


def full_adder(a: int, b: int, carry_in: int) -> tuple[int, int]:
    sum_ab = logic_xor(a, b)
    sum_bit = logic_xor(sum_ab, carry_in)
    carry_out = logic_or(
        logic_and(a, b),
        logic_and(carry_in, sum_ab)
    )
    return sum_bit, carry_out
