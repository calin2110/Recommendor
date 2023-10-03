class CommutativePair:
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2

    def __hash__(self):
        return hash(self.item1) * hash(self.item2)

    def __eq__(self, other):
        if not isinstance(other, CommutativePair):
            return False
        return (self.item1 == other.item1 and self.item2 == other.item2) or \
               (self.item1 == other.item2 and self.item2 == other.item1)

    def __str__(self):
        return f'({self.item1},{self.item2})'
