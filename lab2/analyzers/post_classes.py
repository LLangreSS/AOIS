def preserves_zero(results: list[int]) -> bool:
    return results[0] == 0


def preserves_one(results: list[int]) -> bool:
    return results[-1] == 1


def is_self_dual(results: list[int]) -> bool:
    n = len(results)
    for i in range(n // 2):
        if results[i] == results[n - 1 - i]:
            return False
    return True


def is_monotonic(results: list[int]) -> bool:
    n = len(results)
    for i in range(n):
        for j in range(i + 1, n):
            if (i & j) == i:
                if results[i] > results[j]:
                    return False
    return True


def analyze_post_classes(results: list[int], zhegalkin_coeffs: list[int]) -> dict[str, bool]:
    """
    Возвращает словарь с результатами проверок на классы Поста.
    """
    from analyzers.zhegalkin import is_linear

    return {
        "T0": preserves_zero(results),
        "T1": preserves_one(results),
        "S": is_self_dual(results),
        "M": is_monotonic(results),
        "L": is_linear(zhegalkin_coeffs)
    }
