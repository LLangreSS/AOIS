PRECEDENCE = {
    '!': 5,
    '&': 4,
    '|': 3,
    '->': 2,
    '~': 1
}

ASSOCIATIVITY = {
    '!': 'R',
    '&': 'L',
    '|': 'L',
    '->': 'R',
    '~': 'L'
}


def to_rpn(tokens: list[str]) -> list[str]:
    """
    Переводит список токенов в Обратную Польскую Запись (ОПЗ)
    используя алгоритм сортировочной станции.
    """
    output = []
    operators = []

    for token in tokens:
        if token in "abcde":
            output.append(token)

        elif token in PRECEDENCE:
            while (operators and operators[-1] != '(' and
                   (PRECEDENCE[operators[-1]] > PRECEDENCE[token] or
                    (PRECEDENCE[operators[-1]] == PRECEDENCE[token] and ASSOCIATIVITY[token] == 'L'))):
                output.append(operators.pop())
            operators.append(token)

        elif token == '(':
            operators.append(token)

        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if not operators:
                raise ValueError("Ошибка: пропущена открывающая скобка")
            operators.pop()

    while operators:
        if operators[-1] in '()':
            raise ValueError("Ошибка: пропущена закрывающая скобка")
        output.append(operators.pop())

    return output
