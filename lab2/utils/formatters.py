def print_truth_table(variables: list[str], table: list[dict]):
    """Красивый консольный вывод таблицы истинности."""
    header = " | ".join(variables) + " || F"
    separator = "-" * len(header)

    print(header)
    print(separator)

    for row in table:
        values = [str(row[var]) for var in variables]
        row_str = " | ".join(values) + f" || {row['result']}"
        print(row_str)
