from minimizers.quine_mccluskey import combine, get_prime_implicants, get_minimal_cover, implicants_to_formula
from minimizers.karnaugh import generate_gray_code
from minimizers.quine_mccluskey import print_implicant_table
from minimizers.karnaugh import print_karnaugh_map


def test_combine():
    assert combine("001", "011") == "0-1"
    assert combine("000", "111") is None  # Отличаются в 3 позициях
    assert combine("00-", "01-") == "0--"


def test_get_prime_implicants():
    primes = get_prime_implicants([3], 2)
    assert primes == ["11"]

    primes_or = get_prime_implicants([1, 2, 3], 2)
    assert "-1" in primes_or
    assert "1-" in primes_or


def test_get_minimal_cover():
    primes = ["-1", "1-"]
    indices = [1, 2, 3]
    cover = get_minimal_cover(primes, indices, 2)
    assert "-1" in cover
    assert "1-" in cover


def test_implicants_to_formula():
    assert implicants_to_formula(["1-", "-1"], ['a', 'b']) == "a | b"
    assert implicants_to_formula(["1-0"], ['a', 'b', 'c']) == "(a & !c)"
    assert implicants_to_formula([], ['a', 'b']) == "0"
    assert implicants_to_formula(["--"], ['a', 'b']) == "1"


def test_gray_code():
    code_2 = generate_gray_code(2)
    assert code_2 == ['00', '01', '11', '10']


def test_quine_mccluskey_edge_cases():
    assert get_prime_implicants([], 2) == []
    assert get_minimal_cover([], [], 2) == []
    assert implicants_to_formula([], ['a', 'b']) == "0"

    assert get_prime_implicants([0, 1, 2, 3], 2) == ['--']
    assert get_minimal_cover(['--'], [0, 1, 2, 3], 2) == ['--']
    assert implicants_to_formula(['--'], ['a', 'b']) == "1"


def test_print_implicant_table(capsys):
    primes = ["-1", "1-"]
    indices = [1, 2, 3]
    print_implicant_table(primes, indices, 2)
    captured = capsys.readouterr()
    assert "ИМПЛИКАНТНАЯ ТАБЛИЦА" in captured.out

    print_implicant_table([], [], 2)
    captured = capsys.readouterr()
    assert "не требуется" in captured.out


def test_print_karnaugh_map(capsys):
    mock_table = [
        {'a': 0, 'b': 0, 'result': 0},
        {'a': 0, 'b': 1, 'result': 1},
        {'a': 1, 'b': 0, 'result': 1},
        {'a': 1, 'b': 1, 'result': 1},
    ]
    print_karnaugh_map(['a', 'b'], mock_table)
    captured = capsys.readouterr()
    assert "КАРТА КАРНО" in captured.out
    assert "a\\b" in captured.out

    print_karnaugh_map(['a', 'b', 'c', 'd', 'e', 'f'], [])
    captured = capsys.readouterr()
    assert "поддерживается для 1-5" in captured.out


def test_gray_code_edge_cases():
    assert generate_gray_code(0) == ['']
    assert generate_gray_code(1) == ['0', '1']
