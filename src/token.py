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
TOKEN_NOPOP     = 23
TOKEN_SWAPTOP   = 24
TOKEN_GTE       = 25
TOKEN_LTE       = 26
TOKEN_EQUALS    = 27
TOKEN_STACKLOG  = 28
TOKEN_STORE     = 29
TOKEN_REG       = 30

BUILTIN_WORDS = {
    "print": TOKEN_PRINT,
    "word": TOKEN_WORD_DECL,
    "copy": TOKEN_COPY,
    "+": TOKEN_PLUS,
    "-": TOKEN_MINUS,
    "/": TOKEN_DIVIDE,
    "*": TOKEN_MULTIPLY,
    ">": TOKEN_GREATER,
    ">=": TOKEN_GTE,
    "<": TOKEN_LESS,
    "<=": TOKEN_LTE,
    "=": TOKEN_EQUALS,
    "pop": TOKEN_POP,
    "exec": TOKEN_EXEC,
    "run": TOKEN_RUN,
    "if": TOKEN_IF,
    "ifelse": TOKEN_IFELSE,
    "while": TOKEN_WHILE,
    "[": TOKEN_LBLOCK,
    "]": TOKEN_RBLOCK,
    "nopop": TOKEN_NOPOP,
    "swaptop": TOKEN_SWAPTOP,
    "stacklog": TOKEN_STACKLOG,
    "store": TOKEN_STORE
}

class Token:
    def __init__(self, line: int, id: int, item):
        self.id = id
        self.line = line
        self.item = item
        
    def __str__(self):
        return "<Token id={}. item={}, line={}>".format(self.id, self.item, self.line)
    __repr__ = __str__