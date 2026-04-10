class QuineMcCluskey:
    """Сервис для минимизации логических функций (GRASP: Pure Fabrication)"""

    @staticmethod
    def get_diff(a, b):
        """Находит различие в один бит между двумя бинарными строками."""
        diff_count = 0
        pos = -1
        for i in range(len(a)):
            if a[i] != b[i]:
                diff_count += 1
                pos = i
        return pos if diff_count == 1 else -1

    def minimize(self, num_vars, minterms):
        if not minterms: return "0"

        groups = {}
        for m in minterms:
            res = bin(m)[2:].zfill(num_vars)
            ones = res.count('1')
            groups.setdefault(ones, set()).add(res)

        all_prime_implicants = set()

        while groups:
            new_groups = {}
            marked = set()
            keys = sorted(groups.keys())

            for i in range(len(keys) - 1):
                for term1 in groups[keys[i]]:
                    for term2 in groups[keys[i + 1]]:
                        pos = self.get_diff(term1, term2)
                        if pos != -1:
                            new_term = term1[:pos] + '-' + term1[pos + 1:]
                            new_groups.setdefault(keys[i], set()).add(new_term)
                            marked.add(term1)
                            marked.add(term2)

            for g in groups.values():
                for term in g:
                    if term not in marked:
                        all_prime_implicants.add(term)
            groups = new_groups

        return " | ".join(all_prime_implicants) if all_prime_implicants else "1"
