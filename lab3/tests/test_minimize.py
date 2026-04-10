import pytest
from src.minimizer import QuineMcCluskey
from src.ods3_minimizer import OneBitAdder
from src.t_minimizer import TCounter8
from src.visual import FormulaFormatter


class TestQuineMcCluskey:
    @pytest.fixture
    def qm(self):
        return QuineMcCluskey()

    def test_minimize_constant_zero(self, qm):
        assert qm.minimize(3, []) == "0"

    def test_minimize_simple_and(self, qm):
        assert qm.minimize(2, [3]) == "11"

    def test_minimize_reduction(self, qm):
        assert qm.minimize(2, [2, 3]) == "1-"

    def test_get_diff(self, qm):
        assert qm.get_diff("110", "111") == 2
        assert qm.get_diff("110", "000") == -1


class TestFormatter:
    @pytest.fixture
    def fmt(self):
        return FormulaFormatter()

    def test_format_constant_one(self, fmt):
        assert fmt.format("1", ["A", "B"]) == "1"
        assert fmt.format("---", ["A", "B", "C"]) == "1"

    def test_format_complex_logic(self, fmt):
        assert fmt.format("1-0", ["X", "Y", "Z"]) == "X * !Z"

    def test_format_multiple_terms(self, fmt):
        assert fmt.format("11 | 00", ["A", "B"]) == "A * B + !A * !B"


class TestDevices:
    @pytest.fixture
    def qm(self):
        return QuineMcCluskey()

    def test_adder_synthesis_logic(self, qm):
        adder = OneBitAdder(qm)
        results = adder.synthesize()
        assert len(results["Cout (P)"].split(" | ")) == 3
        assert len(results["Sum (S)"].split(" | ")) == 4

    def test_counter_synthesis_logic(self, qm):
        counter = TCounter8(qm)
        results = counter.synthesize()
        assert results["T0"] == "---"
        assert results["T1"] == "--1"
        assert results["T2"] == "-11"


def test_formatter_mismatch_length():
    fmt = FormulaFormatter()
    with pytest.raises(IndexError):
        fmt.format("111", ["A", "B"])
