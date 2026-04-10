from core.lexer import tokenize
from core.parser import to_rpn
from core.truth_table import generate_truth_table
from utils.formatters import print_truth_table
from analyzers.basic_forms import get_index_form, get_numeric_forms, build_sdnf, build_sknf
from analyzers.zhegalkin import get_zhegalkin_coefficients, build_zhegalkin_polynomial
from analyzers.post_classes import analyze_post_classes
from analyzers.dummy_variables import find_dummy_variables
from analyzers.derivatives import get_derivative_reduced  
from minimizers.quine_mccluskey import get_prime_implicants, print_implicant_table
from minimizers.karnaugh import print_karnaugh_map
from minimizers.quine_mccluskey import get_minimal_cover, implicants_to_formula


def main():
    user_input = input("\nВведите логическое выражение: ").strip()

    if not user_input:
        expression = "a -> (b | !c)"
        print(f"Пустой ввод. Используем выражение по умолчанию: {expression}")
    else:
        expression = user_input

    print(f"Анализируем функцию: {expression}\n")

    tokens = tokenize(expression)
    rpn = to_rpn(tokens)
    variables, truth_table = generate_truth_table(rpn)

    print("ТАБЛИЦА ИСТИННОСТИ:")
    print_truth_table(variables, truth_table)
    print("-" * 40)

    binary_index, decimal_index = get_index_form(truth_table)
    sdnf_num, sknf_num = get_numeric_forms(truth_table)

    print(f"Индексная форма: {binary_index} (десятичное: {decimal_index})")
    print(f"Числовая форма СДНФ: ∑({', '.join(map(str, sdnf_num))})")
    print(f"Числовая форма СКНФ: ∏({', '.join(map(str, sknf_num))})")

    print("\nСДНФ:")
    print(build_sdnf(variables, truth_table))
    print("\nСКНФ:")
    print(build_sknf(variables, truth_table))
    print("-" * 40)

    results = [row['result'] for row in truth_table]
    z_coeffs = get_zhegalkin_coefficients(results)

    print("\n" + "=" * 40)
    print("АНАЛИЗ ФУНКЦИИ")
    print("=" * 40)

    print(f"Полином Жегалкина:\n{build_zhegalkin_polynomial(variables, z_coeffs)}")

    dummies = find_dummy_variables(variables, z_coeffs)
    print(f"\nФиктивные переменные: {', '.join(dummies) if dummies else 'Нет'}")

    post_classes = analyze_post_classes(results, z_coeffs)
    print("\nПринадлежность к классам Поста:")
    for post_class, belongs in post_classes.items():
        print(f"Класс {post_class}: {'+' if belongs else '-'}")

    print("\n" + "=" * 40)
    print("БУЛЕВА ДИФФЕРЕНЦИАЦИЯ")
    print("=" * 40)

    current_vector = results
    current_vars = variables.copy()

    for i in range(len(variables)):
        target = current_vars[0]

        current_vector, current_vars = get_derivative_reduced(current_vector, current_vars, target)

        order = i + 1
        print(f"\n{order}. Производная {order}-го порядка по {target}:")
        print(f"Вектор: {''.join(map(str, current_vector))}")

        if current_vars:
            d_table = []
            for idx, val in enumerate(current_vector):
                bin_str = bin(idx)[2:].zfill(len(current_vars))
                row = {current_vars[j]: int(bin_str[j]) for j in range(len(current_vars))}
                row['result'] = val
                d_table.append(row)
            print_truth_table(current_vars, d_table)
        else:
            print(f"Результат: константа {current_vector[0]}")
            break

    print("\n" + "=" * 40)
    print("МИНИМИЗАЦИЯ ФУНКЦИИ")
    print("=" * 40)

    num_vars = len(variables)

    print("\n[1] РАСЧЕТНЫЙ МЕТОД")

    print("\n--- Склеивание для ДНФ ---")
    primes_dnf = get_prime_implicants(sdnf_num, num_vars)
    sokr_dnf = implicants_to_formula(primes_dnf, variables, is_cnf=False)

    print("\n--- Склеивание для КНФ ---")
    primes_cnf = get_prime_implicants(sknf_num, num_vars)
    sokr_cnf = implicants_to_formula(primes_cnf, variables, is_cnf=True)

    print(f"\nРезультат расчетного метода (Сокращенная ДНФ):\n{sokr_dnf}")
    print(f"Результат расчетного метода (Сокращенная КНФ):\n{sokr_cnf}")

    print("\n" + "-" * 40)
    print("[2] РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД")

    print("\n--- Импликантная таблица ДНФ ---")
    print_implicant_table(primes_dnf, sdnf_num, num_vars)
    min_cover_dnf = get_minimal_cover(primes_dnf, sdnf_num, num_vars)
    mdnf_formula = implicants_to_formula(min_cover_dnf, variables, is_cnf=False)

    print("\n--- Импликантная таблица КНФ ---")
    print_implicant_table(primes_cnf, sknf_num, num_vars)
    min_cover_cnf = get_minimal_cover(primes_cnf, sknf_num, num_vars)
    mknf_formula = implicants_to_formula(min_cover_cnf, variables, is_cnf=True)

    print(f"\nРезультат расчетно-табличного метода (МДНФ):\n{mdnf_formula}")
    print(f"Результат расчетно-табличного метода (МКНФ):\n{mknf_formula}")

    print("\n" + "-" * 40)
    print("[3] ТАБЛИЧНЫЙ МЕТОД (КАРТА КАРНО)")

    print_karnaugh_map(variables, truth_table)

    print(f"\nРезультат минимизации по Карте Карно (МДНФ):\n{mdnf_formula}")
    print(f"Результат минимизации по Карте Карно (МКНФ):\n{mknf_formula}")

    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
