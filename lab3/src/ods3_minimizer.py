class OneBitAdder:
    """Модель ОДС-3 (SOLID: Information Expert)"""

    def __init__(self, minimizer):
        self.minimizer = minimizer
        self.num_vars = 3

    def get_sdnf_indices(self):
        sum_indices = []
        cout_indices = []
        for i in range(8):
            a, b, cin = (i >> 2) & 1, (i >> 1) & 1, i & 1
            s = a ^ b ^ cin
            c = (a & b) | (cin & (a ^ b))
            if s: sum_indices.append(i)
            if c: cout_indices.append(i)
        return sum_indices, cout_indices

    def synthesize(self):
        s_idx, c_idx = self.get_sdnf_indices()
        return {
            "Sum (S)": self.minimizer.minimize(self.num_vars, s_idx),
            "Cout (P)": self.minimizer.minimize(self.num_vars, c_idx)
        }
