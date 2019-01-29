from src import token
from src import  block

# Internal token ID's. Don't use these
TOKEN_BLOCK_START = -1
WHITESPACE = "\t\n "

class Scanner:
    def __init__(self, source, emit_block_tokens=False):
        self.source = source + "\0"
        self.start = 0
        self.stop = 0
        # Whether to parse [ symbols or just emit them as tokens
        self.ebt = emit_block_tokens

    def __current(self):
        return self.source[self.stop]

    @property
    def __sub(self):
        return self.source[self.start:self.stop]

    @property
    def __at_end(self):
        return self.source[self.stop] == "\0"

    def __iter__(self):
        return self

    def __next__(self, block=None):
        if block:
            return next(block)

        while self.__current() in WHITESPACE:
            self.start += 1
            self.stop += 1

        if self.__at_end:
            raise StopIteration
        elif self.__current() in "0123456789.":
            return self.__parse_number()
        elif self.__current() == "#":
            self.__parse_comment()
            return next(self)
        return self.__parse_word()

    def __parse_number(self):
        while self.source[self.stop] in "0123456789.":
            self.stop += 1
        
        dots = sum(1 for _ in self.__sub if _ == ".")
        tok = None
        if dots > 1:
            raise Exception("Too many decimals in floating point literal")
        elif dots == 1:
            tok = token.Token(token.TOKEN_FLOAT, float(self.__sub))
        else:
            tok = token.Token(token.TOKEN_INT, int(self.__sub))
        self.stop += 1
        return tok

    def __parse_comment(self):
        first_go = True # so I can chomp past first `#' char
        while self.source[self.stop] != "#" or first_go:
            first_go = False
            self.stop += 1
        self.stop += 1
        if self.__at_end:
            raise StopIteration
        self.stop += 1
        self.start = self.stop

    def __parse_word(self):
        pass
