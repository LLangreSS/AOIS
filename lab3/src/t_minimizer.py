class TCounter8:
    """Модель счетчика (SOLID: Open/Closed - легко расширить до 16 состояний)"""

    def __init__(self, minimizer):
        self.minimizer = minimizer
        self.num_vars = 3

    def get_t_excitation_minterms(self):
        t_inputs = {"T2": [], "T1": [], "T0": []}
        for current_state in range(8):
            next_state = (current_state + 1) % 8

            c2, c1, c0 = (current_state >> 2) & 1, (current_state >> 1) & 1, current_state & 1
            n2, n1, n0 = (next_state >> 2) & 1, (next_state >> 1) & 1, next_state & 1

            if c2 != n2: t_inputs["T2"].append(current_state)
            if c1 != n1: t_inputs["T1"].append(current_state)
            if c0 != n0: t_inputs["T0"].append(current_state)
        return t_inputs

    def synthesize(self):
        inputs = self.get_t_excitation_minterms()
        results = {}
        for name, minterms in inputs.items():
            results[name] = self.minimizer.minimize(self.num_vars, minterms)
        return results
