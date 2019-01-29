#!/usr/bin/python3
from src.scanner import Scanner
from src.runner import run
from src.vm import VM
from src.token import *
import sys, readline

def run_source(source, vm):
    scan = Scanner(source)
    oldvm = vm
    try:
        for tok in scan:
            try:
                run(vm, tok, lambda:next(scan))
            except Exception as e:
                print("Runtime Error:", e, file=sys.stderr)
                return oldvm, True
    except Exception as e:
        print("Lexing Error:", e, file=sys.stderr)
        return oldvm, True
    return vm, False

if len(sys.argv) == 1:
    print("Welcome to the PyJeru REPL")
    vm = VM()
    while 1:
        text = input(">>> ")
        if len(text) == 0:
            continue
        if text[0] == "?":
            readline.add_history(text)
            text = text[1:]
        vm, error = run_source(text, vm)
        if not error:
            print()
            vm.log()
    
else:
    vm = VM()
    for file in sys.argv[1:]:
        with open(file) as f:
            vm, error = run_source(f.read(), vm)
            if error:
                break
                

