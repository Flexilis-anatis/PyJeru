from src import token
from src.block import Block

# Internal token ID's. Don't use these
TOKEN_BLOCK_START = -1
WHITESPACE = "\t\n "

class Scanner:
    def __init__(self, source):
        self.source = source + "\0"
        self.start = 0
        self.stop = 0
        self.line = 1
        # Whether to parse [ chars or just emit them
        self.emit_block_tokens = False

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

    def __next__(self):
        self.start = self.stop
        while self.__current() in WHITESPACE:
            if self.__current() == "\n":
                self.line += 1
            self.start += 1
            self.stop += 1

        if self.__at_end:
            raise StopIteration
        elif self.__current() in "0123456789.":
            return self.__parse_number()
        elif self.__current() == "#":
            self.__parse_comment()
            return next(self)
        elif self.__current() == "\"":
            return self.__parse_string()
        return self.__parse_word()

    def __parse_number(self):
        while self.source[self.stop] in "0123456789.":
            self.stop += 1

        dots = sum(1 for _ in self.__sub if _ == ".")
        tok = None
        if dots > 1:
            raise Exception(
                "[line {}] Too many decimals in floating point literal". \
                   format(self.line)
            )
        elif dots == 1:
            tok = token.Token(self.line, token.TOKEN_FLOAT, float(self.__sub))
        else:
            tok = token.Token(self.line, token.TOKEN_INT, int(self.__sub))
        if not self.__at_end: self.stop += 1
        return tok

    def __parse_comment(self):
        sstart_line = self.line
        first_go = True # so I can chomp past first `#' char
        while not self.__at_end and self.source[self.stop] != "#" or first_go:
            if self.__current() == "\n":
                self.line += 1
            first_go = False
            self.stop += 1
        if self.__at_end:
            raise Exception("[line {}] unterminated comment".format(start_line))
        self.stop += 1
        if self.__at_end:
            raise StopIteration
        self.stop += 1

    def __parse_word(self, emit_block_tokens=False):
        while (not self.__at_end) and (self.__current() not in WHITESPACE):
            self.stop += 1
        tok = token.Token(self.line,
                          token.BUILTIN_WORDS.get(self.__sub,
                                                  token.TOKEN_WORD),
                          self.__sub)
        if not self.emit_block_tokens:
            if tok.id == token.TOKEN_LBLOCK:
                tok.item = self.__parse_block(self.line)
                tok.id = token.TOKEN_BLOCK

        return tok

    def __parse_string(self):
        first_go = True
        start_line = self.line
        while not self.__at_end and self.__current() != "\"" or first_go:
            if self.__current() == "\n":
                self.line += 1
            first_go = False
            self.stop += 1
        self.start += 1
        if self.__at_end:
            raise Exception("[line {}] unterminated string".format(start_line))
        tok = token.Token(self.line, token.TOKEN_STRING,
                          bytes(self.__sub, "utf-8").decode("unicode_escape"))
        self.stop += 1
        return tok

    def __parse_block(self, line, noerror=False):
        tokens = []
        self.emit_block_tokens = True
        error = True
        for tok in self:
            if tok.id == token.TOKEN_LBLOCK:
                tok.item = self.__parse_block(-1, True);
                self.emit_block_tokens = True
                tok.id = token.TOKEN_BLOCK
            elif tok.id == token.TOKEN_RBLOCK:
                error = False
                break
            tokens.append(tok)
        if self.__at_end and error and not noerror:
            raise Exception("[line {}] Unmatched [".format(line))
        self.emit_block_tokens = False
        return Block(tokens)
