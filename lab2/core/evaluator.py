def evaluate_rpn(rpn: list[str], context: dict[str, int]) -> int:
    """
    Вычисляет значение выражения в формате ОПЗ
    на основе словаря значений переменных (context).
    """
    stack = []

    for token in rpn:
        if token in "abcde":
            stack.append(context[token])
        elif token == '!':
            val = stack.pop()
            stack.append(int(not val))
        else:
            right = stack.pop()
            left = stack.pop()

            if token == '&':
                stack.append(left & right)
            elif token == '|':
                stack.append(left | right)
            elif token == '->':
                stack.append(int(left <= right))
            elif token == '~':
                stack.append(int(left == right))

    return stack[0]
