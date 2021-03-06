def lex_to_string(item):
    lexeme = str(item)
    if isinstance(item, str):
        lexeme = repr(item)
    return lexeme

class VM:
    def __init__(self):
        self.words = {}
        self.data_stack = []
        self.code_stack = []

    def log(self):
        if len(self.data_stack) == 0:
            print("[],", len(self.code_stack))
            return
        string = "["
        for data in self.data_stack:
            string += lex_to_string(data) + ", "
        string = string[:-2] + "], " + str(len(self.code_stack))
        print(string)