#!/usr/bin/python3
from src.scanner import Scanner
from src.token import *

def lex_to_string(tok):
    lexeme = "'" + str(tok.item) + "'"
    if tok.id == TOKEN_STRING:
        lexeme = repr(tok.item)
    elif tok.id == TOKEN_BLOCK:
        lexeme = "["
        for subtok in tok.item:
            lexeme += lex_to_string(subtok) + ", "
        lexeme = lexeme[:-2] + "]"
    return lexeme

scan = Scanner("#comment# 3 word [ print [ pop test ] ] ] hi \n\"str\\nt\" #comment again#")
iters = 20
try:
    for tok in scan:
        iters -= 1
        if not iters:
            break
        print(lex_to_string(tok))
except Exception as e:
    import sys
    print("Error:", e, file=sys.stderr)
