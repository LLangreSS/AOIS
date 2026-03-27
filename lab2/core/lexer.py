def tokenize(expression: str) -> list[str]:
    """
    Разбивает логическое выражение на токены.
    Поддерживает переменные a-e, скобки и операторы: &, |, !, ->, ~
    """
    tokens = []
    i = 0
    expr = expression.replace(" ", "")

    while i < len(expr):
        char = expr[i]

        if char in "abcde()!&|~":
            tokens.append(char)
            i += 1

        elif char == "-" and i + 1 < len(expr) and expr[i + 1] == ">":
            tokens.append("->")
            i += 2
        else:
            raise ValueError(f"Неизвестный символ или ошибка синтаксиса на индексе {i}: '{char}'")

    return tokens
