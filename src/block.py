class Block:
    def __init__(self, tokens: list):
        self.tokens: list = tokens
        self.instruct: int = 0

    def __next__(self):
        self.instruct += 1
        if self.instruct > len(self.tokens):
            raise StopIteration
        return self.tokens[self.instruct-1]

    def copy(self):
        return Block(self.tokens)