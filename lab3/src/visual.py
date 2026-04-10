class FormulaFormatter:
    """Отвечает за визуальное представление формул (SOLID: Single Responsibility)"""

    @staticmethod
    def format(mask_string, var_names):
        if mask_string == "---" or mask_string == "1": return "1"
        if mask_string == "0": return "0"

        terms = mask_string.split(" | ")
        formatted_terms = []

        for term in terms:
            parts = []
            for i, char in enumerate(term):
                if char == '1':
                    parts.append(var_names[i])
                elif char == '0':
                    parts.append(f"!{var_names[i]}")
            formatted_terms.append(" * ".join(parts))

        return " + ".join(formatted_terms)
