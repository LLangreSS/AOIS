import pytest
from core.lexer import tokenize
from core.parser import to_rpn
from core.evaluator import evaluate_rpn
from core.truth_table import extract_variables, generate_truth_table


@pytest.mark.parametrize("expr, expected", [
    ("a & b", ['a', '&', 'b']),
    ("!(a -> b) | ~c", ['!', '(', 'a', '->', 'b', ')', '|', '~', 'c']),
    ("a->b", ['a', '->', 'b']),
])
def test_tokenize_valid(expr, expected):
    assert tokenize(expr) == expected


def test_tokenize_invalid():
    with pytest.raises(ValueError, match="Неизвестный символ"):
        tokenize("a + b")


@pytest.mark.parametrize("tokens, expected", [
    (['a', '&', 'b'], ['a', 'b', '&']),
    (['!', 'a'], ['a', '!']),
    (['a', '->', '(', 'b', '|', 'c', ')'], ['a', 'b', 'c', '|', '->']),
])
def test_to_rpn_valid(tokens, expected):
    assert to_rpn(tokens) == expected


def test_to_rpn_unmatched_brackets():
    with pytest.raises(ValueError):
        to_rpn(['(', 'a', '&', 'b'])
    with pytest.raises(ValueError):
        to_rpn(['a', '&', 'b', ')'])


@pytest.mark.parametrize("rpn, context, expected", [
    (['a', 'b', '&'], {'a': 1, 'b': 1}, 1),
    (['a', 'b', '&'], {'a': 1, 'b': 0}, 0),
    (['a', 'b', '|'], {'a': 0, 'b': 1}, 1),
    (['a', '!'], {'a': 1}, 0),
    (['a', 'b', '->'], {'a': 1, 'b': 0}, 0),
    (['a', 'b', '->'], {'a': 0, 'b': 1}, 1),
    (['a', 'b', '~'], {'a': 1, 'b': 1}, 1),
    (['a', 'b', '~'], {'a': 1, 'b': 0}, 0),
])
def test_evaluate_rpn(rpn, context, expected):
    assert evaluate_rpn(rpn, context) == expected


def test_generate_truth_table():
    rpn = ['a', 'b', '->']
    vars_list, table = generate_truth_table(rpn)

    assert vars_list == ['a', 'b']
    assert len(table) == 4
    assert table[2] == {'a': 1, 'b': 0, 'result': 0}
