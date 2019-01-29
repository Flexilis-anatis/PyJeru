#!/usr/bin/python3
from src import scanner

scan = scanner.Scanner("#comment# 5 #comment again#")
iters = 20
for tok in scan:
    iters -= 1
    if not iters:
        break
    print(tok.item)