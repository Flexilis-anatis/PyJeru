TOKEN_INT = 0
TOKEN_FLOAT = 1
TOKEN_STRING = 2
TOKEN_PRINT = 3
TOKEN_BLOCK = 4

class Token:
    def __init__(self, id: int, item):
        self.id = id
        self.item = item