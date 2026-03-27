def get_zhegalkin_coefficients(results: list[int]) -> list[int]:
    """
    Вычисляет коэффициенты полинома Жегалкина методом треугольника.
    """
    coeffs = [results[0]]
    current_row = results.copy()

    while len(current_row) > 1:
        next_row = [current_row[i] ^ current_row[i + 1] for i in range(len(current_row) - 1)]
        coeffs.append(next_row[0])
        current_row = next_row

    return coeffs


def build_zhegalkin_polynomial(variables: list[str], coeffs: list[int]) -> str:
    """
    Строит строковое представление полинома Жегалкина.
    """
    terms = []
    n = len(variables)

    for i, coeff in enumerate(coeffs):
        if coeff == 1:
            if i == 0:
                terms.append("1")
            else:
                bin_str = bin(i)[2:].zfill(n)
                term_vars = [variables[j] for j, bit in enumerate(bin_str) if bit == '1']
                terms.append("(" + " & ".join(term_vars) + ")")

    if not terms:
        return "0"

    return " ^ ".join(terms)


def is_linear(coeffs: list[int]) -> bool:
    """
    Проверяет линейность функции по коэффициентам Жегалкина.
    Если есть хоть один коэффициент = 1 для слагаемого с более чем одной переменной,
    функция нелинейна.
    """
    for i, coeff in enumerate(coeffs):
        if coeff == 1 and bin(i).count('1') > 1:
            return False
    return True
