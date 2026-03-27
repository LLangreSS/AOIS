from core.evaluator import evaluate_rpn


def extract_variables(rpn: list[str]) -> list[str]:
    """Извлекает уникальные переменные из ОПЗ и сортирует их по алфавиту."""
    return sorted(list(set([t for t in rpn if t in "abcde"])))


def generate_truth_table(rpn: list[str]) -> tuple[list[str], list[dict]]:
    """
    Строит таблицу истинности.
    Возвращает список переменных и список строк таблицы.
    Каждая строка - это словарь с ключами: переменные и 'result'.
    """
    variables = extract_variables(rpn)
    n = len(variables)
    total_rows = 2 ** n

    table = []

    for i in range(total_rows):
        binary_str = bin(i)[2:].zfill(n)

        context = {variables[j]: int(binary_str[j]) for j in range(n)}

        result = evaluate_rpn(rpn, context)

        row = context.copy()
        row['result'] = result
        table.append(row)

    return variables, table
