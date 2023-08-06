import random


class Dice:
    def __init__(self, n_dice=2):
        self.n_dice = n_dice
        self._values = []

    def roll(self):
        self._values = [random.randint(1, 6) for i in range(self.n_dice)]
        return sum(self._values)

    def is_doubles(self):
        return self.n_dice >= 2 and self._values[0] == self._values[1]


def test_dice():
    d = Dice(2)
    print("Rolling dice...")
    for i in range(10):
        print(d.roll())


if __name__ == "__main__":
    test_dice()
