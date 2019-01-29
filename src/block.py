class Block:
    def __init__(self, toks):
        self.toks = toks
        self.at = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.at >= len(self.toks):
            raise StopIteration
        t = self.toks[self.at]
        self.at += 1
        return t
    def __call__(self):
        return Block(self.toks[:])
