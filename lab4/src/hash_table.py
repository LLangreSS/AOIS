from enum import Enum


class State(Enum):
    EMPTY = 0
    OCCUPIED = 1
    DELETED = 2


class HashEntry:
    def __init__(self):
        self.state = State.EMPTY
        self.key = None
        self.v = None
        self.h_base = None
        self.data = None
        self.probes = 0


class HashTable:
    def __init__(self, size=23):
        self.size = size
        self.table = [HashEntry() for _ in range(size)]
        self.count = 0
        self.prime = 17

    def _calc_v(self, key):
        return sum(ord(char) for char in key)

    def _hash1(self, v):
        return v % self.size

    def _hash2(self, v):
        return self.prime - (v % self.prime)

    def insert(self, key, data):
        """Добавление новой записи. Если ключ есть — ошибка."""
        if self.count >= self.size:
            return False

        v = self._calc_v(key)
        h_base = self._hash1(v)
        step = self._hash2(v)

        index = h_base
        for i in range(self.size):
            entry = self.table[index]
            if entry.state == State.EMPTY: break
            if entry.state == State.OCCUPIED and entry.key == key:
                print(f"Ошибка: Ключ '{key}' уже существует!")
                return False
            index = (h_base + (i + 1) * step) % self.size

        index, probes = h_base, 0
        while self.table[index].state == State.OCCUPIED:
            probes += 1
            index = (h_base + probes * step) % self.size

        e = self.table[index]
        e.state, e.key, e.v, e.h_base, e.data, e.probes = State.OCCUPIED, key, v, h_base, data, probes
        self.count += 1
        return True

    def search(self, key):
        """Поиск объекта записи по ключевому слову."""
        v = self._calc_v(key)
        h_base, step = self._hash1(v), self._hash2(v)
        idx = h_base
        for i in range(self.size):
            entry = self.table[idx]
            if entry.state == State.EMPTY:
                return None
            if entry.state == State.OCCUPIED and entry.key == key:
                return entry
            idx = (h_base + (i + 1) * step) % self.size
        return None

    def update(self, key, new_data):
        """Обновление данных по существующему ключу."""
        entry = self.search(key)
        if entry:
            entry.data = new_data
            print(f">>> Данные для '{key}' успешно изменены.")
            return True
        print(f"!!! Ошибка: Ключ '{key}' не найден для обновления.")
        return False

    def delete(self, key):
        v = self._calc_v(key)
        h_base, step = self._hash1(v), self._hash2(v)
        index = h_base
        for i in range(self.size):
            entry = self.table[index]
            if entry.state == State.EMPTY: return False
            if entry.state == State.OCCUPIED and entry.key == key:
                entry.state, entry.key, entry.v, entry.h_base, entry.data = State.DELETED, None, None, None, None
                self.count -= 1
                return True
            index = (h_base + (i + 1) * step) % self.size
        return False

    def display(self):
        print("\n" + "-" * 115)
        print(
            f"| {'Индекс':^6} | {'Статус':^8} | {'Ключ (ID)':^15} | {'V(K)':^6} | {'h(V)':^4} | {'Шаги':^4} | {'Данные (Pi)':^45} |")
        print("-" * 115)
        for i in range(self.size):
            e = self.table[i]
            st = e.state.name
            if e.state == State.OCCUPIED:
                print(f"| {i:^6} | {st:^8} | {e.key:<15} | {e.v:^6} | {e.h_base:^4} | {e.probes:^4} | {e.data:<45} |")
            else:
                print(f"| {i:^6} | {st:^8} | {'---':^15} | {'---':^6} | {'---':^4} | {'---':^4} | {'---':<45} |")
        print("-" * 115)
        print(f"Коэффициент заполнения: {self.count / self.size:.2f}")
