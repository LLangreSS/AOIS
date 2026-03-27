def get_index_form(table: list[dict]) -> tuple[str, int]:
    """
    Возвращает индексную форму: бинарную строку (вектор функции) и её десятичное значение.
    """
    binary_index = "".join(str(row['result']) for row in table)
    decimal_index = int(binary_index, 2)
    return binary_index, decimal_index


def get_numeric_forms(table: list[dict]) -> tuple[list[int], list[int]]:
    """
    Возвращает числовые формы: списки индексов (номеров строк) для СДНФ (где F=1) и СКНФ (где F=0).
    """
    sdnf_indices = [i for i, row in enumerate(table) if row['result'] == 1]
    sknf_indices = [i for i, row in enumerate(table) if row['result'] == 0]
    return sdnf_indices, sknf_indices


def build_sdnf(variables: list[str], table: list[dict]) -> str:
    """
    Строит СДНФ (Совершенную дизъюнктивную нормальную форму).
    Берем строки, где результат 1. Переменная без отрицания, если 1, с отрицанием, если 0.
    """
    terms = []
    for row in table:
        if row['result'] == 1:
            term_vars = []
            for var in variables:
                term_vars.append(var if row[var] == 1 else f"!{var}")
            terms.append("(" + " & ".join(term_vars) + ")")

    if not terms:
        return "0"

    return " | ".join(terms)


def build_sknf(variables: list[str], table: list[dict]) -> str:
    """
    Строит СКНФ (Совершенную конъюнктивную нормальную форму).
    Берем строки, где результат 0. Переменная без отрицания, если 0, с отрицанием, если 1.
    """
    terms = []
    for row in table:
        if row['result'] == 0:
            term_vars = []
            for var in variables:
                term_vars.append(var if row[var] == 0 else f"!{var}")
            terms.append("(" + " | ".join(term_vars) + ")")

    if not terms:
        return "1"

    return " & ".join(terms)
