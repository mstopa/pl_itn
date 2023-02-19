class UppercaseRestorer:
    def __init__(self, original: str, normalized: str):
        """
        Restore uppercase letters after inverse text normalization.
        UppercaseRestorer looks for words that have been lowercased but not inverse normalized.
        See params' description below for examples.

        params:
        original:   Input phrase, for example "It's half past nine Dave"
        normalized: ITN output phrase, for example "it's 9:30 dave"
        """
        self.original = original.split()
        self.normalized = normalized.split()
        self.restored = self.normalized[:]

        self.original_index = 0
        self.normalized_index = 0

        self.normalized_limit = len(self.normalized)
        self.original_limit = len(self.original)

    def run(self):
        while not self.finished():
            self.step()
        return " ".join(self.restored)

    def step(self):
        # check current pair
        if self.match():
            self.restore()
            return

        # check the next pair
        self.next_original_index()
        self.next_normalized_index()
        if self.match():
            self.restore()
            return

        # look for shifted match
        checkpoint = self.original_index
        while self.next_original_index():
            if self.match():
                self.restore()
                return

        # no match, the word has been inverse normalized
        self.original_index = checkpoint
        self.next_normalized_index
        self.next_original_index

    def finished(self):
        return (self.normalized_index >= self.normalized_limit
                or self.original_index >= self.original_limit)

    def match(self):
        if self.finished():  # out of index guardian
            return False
        return self.normalized[self.normalized_index] == self.original[self.original_index].lower()

    def next_original_index(self):
        self.original_index += 1
        return not self.finished()  # False if index out of range

    def next_normalized_index(self):
        self.normalized_index += 1
        return not self.finished()  # False if index out of range

    def restore(self):
        self.restored[self.normalized_index] = self.original[self.original_index]
        self.next_original_index()
        self.next_normalized_index()