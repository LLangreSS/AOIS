from analyzers.basic_forms import get_index_form, get_numeric_forms, build_sdnf, build_sknf
from analyzers.zhegalkin import get_zhegalkin_coefficients, build_zhegalkin_polynomial, is_linear
from analyzers.post_classes import analyze_post_classes
from analyzers.dummy_variables import find_dummy_variables
from analyzers.derivatives import get_derivative_reduced

MOCK_TABLE_AND = [
    {'a': 0, 'b': 0, 'result': 0},
    {'a': 0, 'b': 1, 'result': 0},
    {'a': 1, 'b': 0, 'result': 0},
    {'a': 1, 'b': 1, 'result': 1},
]


def test_basic_forms():
    bin_idx, dec_idx = get_index_form(MOCK_TABLE_AND)
    assert bin_idx == "0001"
    assert dec_idx == 1

    sdnf_num, sknf_num = get_numeric_forms(MOCK_TABLE_AND)
    assert sdnf_num == [3]
    assert sknf_num == [0, 1, 2]

    assert build_sdnf(['a', 'b'], MOCK_TABLE_AND) == "(a & b)"
    assert build_sknf(['a', 'b'], MOCK_TABLE_AND) == "(a | b) & (a | !b) & (!a | b)"


def test_zhegalkin():
    results = [0, 0, 0, 1]
    coeffs = get_zhegalkin_coefficients(results)
    assert coeffs == [0, 0, 0, 1]

    poly = build_zhegalkin_polynomial(['a', 'b'], coeffs)
    assert poly == "(a & b)"
    assert is_linear(coeffs) is False


def test_post_classes():
    results = [0, 0, 0, 1]
    coeffs = [0, 0, 0, 1]
    classes = analyze_post_classes(results, coeffs)

    assert classes["T0"] is True
    assert classes["T1"] is True
    assert classes["S"] is False
    assert classes["M"] is True
    assert classes["L"] is False


def test_dummy_variables():
    coeffs = [0, 0, 1, 0]
    dummies = find_dummy_variables(['a', 'b'], coeffs)
    assert dummies == ['b']


def test_derivatives():
    results = [0, 1, 0, 1]
    new_res, new_vars = get_derivative_reduced(results, ['a', 'b'], 'a')
    assert new_vars == ['b']
    assert new_res == [0, 0]
