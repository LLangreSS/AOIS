import pytest
from src.hash_table import HashTable, State


@pytest.fixture
def table():
    """Фикстура для создания новой таблицы перед каждым тестом."""
    return HashTable(23)


def test_insert_and_search_success(table):
    assert table.insert("Глагол", "Действие") is True
    res = table.search("Глагол")
    assert res is not None
    assert res.data == "Действие"


def test_insert_duplicate_key(table):
    table.insert("Союз", "Первое")
    assert table.insert("Союз", "Второе") is False
    assert table.search("Союз").data == "Первое"
    assert table.count == 1


def test_update_operation(table):
    table.insert("Слово", "Старое")
    assert table.update("Слово", "Новое") is True
    assert table.search("Слово").data == "Новое"
    assert table.update("Призрак", "Данные") is False


def test_collision_logic(table):
    table.insert("Союз", "Данные 1")
    table.insert("Корень", "Данные 2")

    assert table.table[0].key == "Союз"
    assert table.table[8].key == "Корень"
    assert table.table[8].probes == 1
    assert table.search("Корень").data == "Данные 2"


def test_delete_success(table):
    table.insert("Фраза", "Определение")
    assert table.delete("Фраза") is True
    assert table.search("Фраза") is None
    assert table.table[12].state == State.DELETED


def test_delete_non_existent(table):
    assert table.delete("Призрак") is False


def test_search_non_existent(table):
    assert table.search("Ничего") is None


def test_table_full_error(table):
    for i in range(23):
        table.insert(f"К{i}", "Д")
    assert table.insert("Лишний", "Данные") is False


def test_search_full_table_not_found(table):
    for i in range(23):
        table.insert(f"К{i}", "Д")
    assert table.search("Несуществующий") is None


def test_search_through_deleted(table):
    table.insert("Союз", "1")
    table.insert("Корень", "2")
    table.delete("Союз")
    res = table.search("Корень")
    assert res is not None
    assert res.data == "2"


def test_display_coverage(table, capsys):
    table.insert("Занято", "ОК")
    table.insert("Удалено", "ОК")
    table.delete("Удалено")
    table.display()
    captured = capsys.readouterr().out
    assert "OCCUPIED" in captured
    assert "DELETED" in captured
    assert "EMPTY" in captured
    assert "Коэффициент заполнения" in captured
