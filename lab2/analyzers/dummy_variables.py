def find_dummy_variables(variables: list[str], zhegalkin_coeffs: list[int]) -> list[str]:
    """
    Находит фиктивные переменные через коэффициенты полинома Жегалкина.
    Переменная существенна, если она участвует хотя бы в одном слагаемом с ненулевым коэф.
    """
    essential_indices = set()
    n = len(variables)

    for i, coeff in enumerate(zhegalkin_coeffs):
        if coeff == 1 and i > 0:
            bin_str = bin(i)[2:].zfill(n)
            for j, bit in enumerate(bin_str):
                if bit == '1':
                    essential_indices.add(j)

    dummy_vars = [variables[i] for i in range(n) if i not in essential_indices]
    return dummy_vars
