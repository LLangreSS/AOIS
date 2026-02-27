import sys
from core.integer_math import (
    to_direct_code, to_ones_complement, to_twos_complement,
    add as int_add, difference as int_diff, multiply as int_mul, divide as int_div
)
from core.float754 import (
    parse_to_array, array_to_float_str,
    add as float_add, multiply as float_mul, divide as float_div
)
from core.gray_bcd import to_gray_bcd, add as bcd_add


def format_bits(bit_array: list[int]) -> str:
    return "".join(str(b) for b in bit_array)


def format_float754(bit_array: list[int]) -> str:
    bits = format_bits(bit_array)
    return f"{bits[0]} {bits[1:9]} {bits[9:]}"


def handle_integer_math():
    print("\n--- Целочисленная арифметика ---")
    try:
        a = int(input("Введите первое целое число (A): "))
        b = int(input("Введите второе целое число (B): "))
    except ValueError:
        print("Ошибка: введите корректные целые числа.")
        return

    print(f"\n[A = {a}]")
    print(f"Прямой код:       {format_bits(to_direct_code(a))}")
    print(f"Обратный код:     {format_bits(to_ones_complement(a))}")
    print(f"Дополнительный:   {format_bits(to_twos_complement(a))}")

    print(f"\n[B = {b}]")
    print(f"Прямой код:       {format_bits(to_direct_code(b))}")
    print(f"Обратный код:     {format_bits(to_ones_complement(b))}")
    print(f"Дополнительный:   {format_bits(to_twos_complement(b))}")

    print("\n--- Результаты операций ---")

    add_bits, add_dec = int_add(a, b)
    print(f"A + B = {add_dec}")
    print(f"Битовый вид: {format_bits(add_bits)}")

    diff_bits, diff_dec = int_diff(a, b)
    print(f"A - B = {diff_dec}")
    print(f"Битовый вид: {format_bits(diff_bits)}")

    mul_bits, mul_dec = int_mul(a, b)
    print(f"A * B = {mul_dec}")
    print(f"Битовый вид: {format_bits(mul_bits)}")

    if b != 0:
        div_int_bits, div_frac_bits, div_str = int_div(a, b)
        print(f"A / B = {div_str}")
        print(f"Целая часть (биты):   {format_bits(div_int_bits)}")
        print(f"Дробная часть (биты): {format_bits(div_frac_bits)}")
    else:
        print("A / B = Ошибка (Деление на ноль)")


def handle_float754():
    print("\n--- Арифметика IEEE-754 ---")
    a_str = input("Введите первое число с плавающей точкой (A): ")
    b_str = input("Введите второе число с плавающей точкой (B): ")

    arr_a = parse_to_array(a_str)
    arr_b = parse_to_array(b_str)

    print(f"\n[A = {array_to_float_str(arr_a)}]")
    print(f"IEEE-754: {format_float754(arr_a)}")

    print(f"\n[B = {array_to_float_str(arr_b)}]")
    print(f"IEEE-754: {format_float754(arr_b)}")

    print("\n--- Результаты операций ---")

    add_res = float_add(arr_a, arr_b)
    print(f"A + B = {array_to_float_str(add_res)}")
    print(f"Битовый вид: {format_float754(add_res)}")

    mul_res = float_mul(arr_a, arr_b)
    print(f"A * B = {array_to_float_str(mul_res)}")
    print(f"Битовый вид: {format_float754(mul_res)}")

    try:
        div_res = float_div(arr_a, arr_b)
        print(f"A / B = {array_to_float_str(div_res)}")
        print(f"Битовый вид: {format_float754(div_res)}")
    except ValueError as e:
        print(f"A / B = Ошибка ({e})")


def handle_gray_bcd():
    print("\n--- Арифметика Gray BCD ---")
    try:
        a = int(input("Введите первое положительное целое число (A): "))
        b = int(input("Введите второе положительное целое число (B): "))
    except ValueError:
        print("Ошибка: введите корректные целые числа.")
        return

    arr_a = to_gray_bcd(a)
    arr_b = to_gray_bcd(b)

    print(f"\n[A = {a}]")
    print(f"Gray BCD: {format_bits(arr_a)}")

    print(f"\n[B = {b}]")
    print(f"Gray BCD: {format_bits(arr_b)}")

    print("\n--- Результаты операций ---")

    add_bits, add_dec = bcd_add(a, b)
    print(f"A + B = {add_dec}")
    print(f"Битовый вид: {format_bits(add_bits)}")


def main():
    while True:
        print("\n" + "=" * 40)
        print("   СИМУЛЯТОР АЛУ (Архитектура ЭВМ)")
        print("=" * 40)
        print("1. Целочисленная арифметика")
        print("2. Числа с плавающей точкой (IEEE-754)")
        print("3. Двоично-десятичный код (Gray BCD)")
        print("0. Выход")
        print("=" * 40)

        choice = input("Выберите раздел (0-3): ").strip()

        if choice == '1':
            handle_integer_math()
        elif choice == '2':
            handle_float754()
        elif choice == '3':
            handle_gray_bcd()
        elif choice == '0':
            print("Завершение работы программы.")
            sys.exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
