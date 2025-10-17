class RandomizedSet:
    def __init__(self):
        self._list = []
        self._store = {}

    def insert(self, val: int) -> bool:
        if val in self._store:
            return False

        self._store[val] = len(self._list)
        self._list.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self._store:
            return False

        idx, last_element = self._store[val], self._list[-1]
        self._store[last_element], last_element = idx, self._list[idx]
        del self._store[val]
        self._list.pop()
        return True

    def getRandom(self) -> int:
        import random

        return random.choice(self._list)


if __name__ == "__main__":
    randomizedSet = RandomizedSet()
    print(randomizedSet.insert(1), end=" ")
    print(randomizedSet.remove(2), end=" ")
    print(randomizedSet.insert(2), end=" ")
    print(randomizedSet.getRandom(), end=" ")
    print(randomizedSet.remove(1), end=" ")
    print(randomizedSet.insert(2), end=" ")
    print(randomizedSet.getRandom())
