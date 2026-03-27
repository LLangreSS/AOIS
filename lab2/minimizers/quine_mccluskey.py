def combine(t1: str, t2: str) -> str | None:
    """Склеивает два терма, если они отличаются ровно в одной позиции."""
    diff_count = 0
    res = []
    for a, b in zip(t1, t2):
        if a != b:
            diff_count += 1
            res.append('-')
        else:
            res.append(a)
    return "".join(res) if diff_count == 1 else None


def get_prime_implicants(sdnf_indices: list[int], num_vars: int) -> list[str]:
    """
    Расчетный метод: выводит стадии склеивания и возвращает первичные импликанты.
    """
    if not sdnf_indices:
        return []
    if len(sdnf_indices) == 2 ** num_vars:
        return ['-' * num_vars]

    current_terms = {bin(i)[2:].zfill(num_vars) for i in sdnf_indices}
    all_primes = set()
    step = 1

    print("\n--- ЭТАПЫ СКЛЕИВАНИЯ (Расчетный метод) ---")
    while True:
        next_terms = set()
        used = set()
        terms_list = sorted(list(current_terms))

        print(f"\nСтадия {step}:")
        has_combinations = False

        for i in range(len(terms_list)):
            for j in range(i + 1, len(terms_list)):
                t1, t2 = terms_list[i], terms_list[j]
                combo = combine(t1, t2)
                if combo:
                    next_terms.add(combo)
                    used.add(t1)
                    used.add(t2)
                    print(f"  {t1} + {t2} -> {combo}")
                    has_combinations = True

        all_primes.update(current_terms - used)

        if not next_terms:
            if not has_combinations:
                print("  Склеиваний больше нет.")
            break

        current_terms = next_terms
        step += 1

    return sorted(list(all_primes))


def print_implicant_table(primes: list[str], sdnf_indices: list[int], num_vars: int):
    """
    Расчетно-табличный метод: выводит таблицу покрытия импликантами.
    """
    print("\n--- ИМПЛИКАНТНАЯ ТАБЛИЦА ---")
    if not primes or primes == ['-' * num_vars]:
        print("Таблица не требуется (функция тождественно равна 0 или 1).")
        return

    col_width = max(num_vars, 3)
    header = "Импликанта | " + " | ".join(str(i).center(col_width) for i in sdnf_indices)
    print(header)
    print("-" * len(header))

    for p in primes:
        row_str = f"{p:10} | "
        marks = []
        for idx in sdnf_indices:
            b_idx = bin(idx)[2:].zfill(num_vars)
            match = all(p[k] == '-' or p[k] == b_idx[k] for k in range(num_vars))
            marks.append("X".center(col_width) if match else " ".center(col_width))
        print(row_str + " | ".join(marks))


def implicants_to_formula(implicants: list[str], variables: list[str]) -> str:
    """
    Универсальный переводчик: список бинарных строк ['1-0', '0--']
    превращает в алгебраическую формулу: (a & !c) | !a
    """
    if not implicants:
        return "0"
    if implicants == ['-' * len(variables)]:
        return "1"

    terms = []
    for p in implicants:
        parts = []
        for i, char in enumerate(p):
            if char == '1':
                parts.append(variables[i])
            elif char == '0':
                parts.append(f"!{variables[i]}")

        if len(parts) > 1:
            terms.append("(" + " & ".join(parts) + ")")
        elif len(parts) == 1:
            terms.append(parts[0])

    return " | ".join(terms)


def _build_coverage_map(primes: list[str], sdnf_indices: list[int], num_vars: int) -> dict[str, set[int]]:
    """Шаг 1: Строит словарь покрытий { 'импликанта': {наборы, которые она покрывает} }"""
    coverage = {}
    for p in primes:
        covered = set()
        for idx in sdnf_indices:
            b_idx = bin(idx)[2:].zfill(num_vars)
            if all(p[k] == '-' or p[k] == b_idx[k] for k in range(num_vars)):
                covered.add(idx)
        coverage[p] = covered
    return coverage


def _get_essential_primes(coverage: dict[str, set[int]], sdnf_indices: list[int]) -> tuple[list[str], set[int]]:
    """Шаг 2: Находит обязательные (существенные) импликанты (ядра)."""
    index_counts = {idx: 0 for idx in sdnf_indices}
    for cov in coverage.values():
        for idx in cov:
            index_counts[idx] += 1

    essential_primes = []
    uncovered = set(sdnf_indices)

    for p, cov in coverage.items():
        if any(index_counts[idx] == 1 for idx in cov):
            essential_primes.append(p)
            uncovered -= cov

    return essential_primes, uncovered


def _greedy_cover(coverage: dict[str, set[int]], uncovered: set[int], remaining_primes: list[str]) -> list[str]:
    """Шаг 3: Жадный алгоритм для покрытия оставшихся наборов."""
    additional_cover = []
    while uncovered:
        remaining_primes.sort(key=lambda p: len(coverage[p] & uncovered), reverse=True)
        if not remaining_primes:
            break
        best_prime = remaining_primes.pop(0)
        additional_cover.append(best_prime)
        uncovered -= coverage[best_prime]

    return additional_cover


def get_minimal_cover(primes: list[str], sdnf_indices: list[int], num_vars: int) -> list[str]:
    """
    Находит минимальное покрытие (МДНФ) из всех первичных импликант.
    Возвращает список импликант, например: ['1-0', '01-']
    """
    if not primes or primes == ['-' * num_vars]:
        return primes

    coverage = _build_coverage_map(primes, sdnf_indices, num_vars)

    minimal_cover, uncovered = _get_essential_primes(coverage, sdnf_indices)

    if uncovered:
        remaining_primes = [p for p in primes if p not in minimal_cover]
        minimal_cover.extend(_greedy_cover(coverage, uncovered, remaining_primes))

    return minimal_cover

