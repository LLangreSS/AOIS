def generate_gray_code(n: int) -> list[str]:
    """Генерирует последовательность кода Грея для n бит (DRY/KISS)."""
    if n == 0:
        return ['']
    if n == 1:
        return ['0', '1']
    prev = generate_gray_code(n - 1)
    return ['0' + s for s in prev] + ['1' + s for s in reversed(prev)]


def print_karnaugh_map(variables: list[str], truth_table: list[dict]):
    """
    Выводит Карту Карно в консоль.
    Оси разбиваются пополам: например, для 3-х переменных a '\' bc.
    """
    num_vars = len(variables)
    if num_vars > 5 or num_vars < 1:
        print("Карта Карно поддерживается для 1-5 переменных.")
        return

    results_map = {}
    for row in truth_table:
        key = "".join(str(row[v]) for v in variables)
        results_map[key] = row['result']

    print("\n--- КАРТА КАРНО ---")

    row_vars_count = num_vars // 2
    col_vars_count = num_vars - row_vars_count

    row_vars = variables[:row_vars_count]
    col_vars = variables[row_vars_count:]

    row_labels = generate_gray_code(row_vars_count)
    col_labels = generate_gray_code(col_vars_count)

    corner = "".join(row_vars) + "\\" + "".join(col_vars)

    header = f"{corner:^{len(corner) + 2}}| " + " | ".join(col_labels)
    print(header)
    print("-" * len(header))

    for r_label in row_labels:
        row_str = f"{r_label:^{len(corner) + 2}}| "
        cells = []
        for c_label in col_labels:
            bin_index = r_label + c_label
            val = results_map[bin_index]
            cells.append(str(val).center(len(c_label)))
        print(row_str + " | ".join(cells))
