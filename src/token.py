TOKEN_INT       = 0
TOKEN_FLOAT     = 1
TOKEN_STRING    = 2
TOKEN_PRINT     = 3
TOKEN_BLOCK     = 4
TOKEN_WORD      = 5
TOKEN_WORD_DECL = 6
TOKEN_COPY      = 7
TOKEN_PLUS      = 8
TOKEN_MINUS     = 9
TOKEN_DIVIDE    = 10
TOKEN_MULTIPLY  = 11
TOKEN_GREATER   = 12
TOKEN_LESS      = 13
TOKEN_COPY      = 14
TOKEN_POP       = 15
TOKEN_EXEC      = 16
TOKEN_RUN       = 17
TOKEN_IF        = 18
TOKEN_IFELSE    = 19
TOKEN_WHILE     = 20
TOKEN_LBLOCK    = 21
TOKEN_RBLOCK    = 22

BUILTIN_WORDS = {
    "print": TOKEN_PRINT,
    "word": TOKEN_WORD_DECL,
    "copy": TOKEN_COPY,
    "+": TOKEN_PLUS,
    "-": TOKEN_MINUS,
    "/": TOKEN_DIVIDE,
    "*": TOKEN_MULTIPLY,
    ">": TOKEN_GREATER,
    "<": TOKEN_LESS,
    "pop": TOKEN_POP,
    "exec": TOKEN_EXEC,
    "run": TOKEN_RUN,
    "if": TOKEN_IF,
    "ifelse": TOKEN_IFELSE,
    "while": TOKEN_WHILE,
    "[": TOKEN_LBLOCK,
    "]": TOKEN_RBLOCK
}

class Token:
    def __init__(self, line: int, id: int, item):
        self.id = id
        self.line = line
        self.item = item
