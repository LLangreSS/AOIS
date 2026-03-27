def get_derivative_reduced(results: list[int], variables: list[str], target_var: str) -> tuple[list[int], list[str]]:
    """
    Вычисляет частную производную и ВОЗВРАЩАЕТ уменьшенный вектор и новый список переменных.
    """
    n = len(variables)
    var_idx = variables.index(target_var)
    bit_pos = n - 1 - var_idx
    step = 1 << bit_pos

    new_results = []
    new_vars = [v for v in variables if v != target_var]

    for i in range(1 << n):
        if (i & step) == 0:
            j = i | step
            new_results.append(results[i] ^ results[j])

    return new_results, new_vars
