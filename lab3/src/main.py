from src.minimizer import QuineMcCluskey
from src.ods3_minimizer import OneBitAdder
from src.t_minimizer import TCounter8
from visual import FormulaFormatter

if __name__ == "__main__":
    minimizer = QuineMcCluskey()
    formatter = FormulaFormatter()

    print("=== Синтез ОДС-3 ===")
    adder = OneBitAdder(minimizer)
    adder_vars = ["A", "B", "Cin"]
    for output, logic in adder.synthesize().items():
        formula = formatter.format(logic, adder_vars)
        print(f"{output} = {formula}")

    print("\n=== Синтез счетчика (T-триггеры) ===")
    counter = TCounter8(minimizer)
    counter_vars = ["Q2", "Q1", "Q0"]
    for t_input, logic in counter.synthesize().items():
        formula = formatter.format(logic, counter_vars)
        print(f"{t_input} = {formula}")