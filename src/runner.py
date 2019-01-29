from src import token
from copy import deepcopy

def mathop(vm, tok, intop, floatop, nopop):
    if len(vm.data_stack) < 2:
        raise Exception("[line {}] need two operands for binary operator {}".format(tok.line, tok.item))
    if isinstance(vm.data_stack[-1], float):
        vm.data_stack[-2] = float(vm.data_stack[-2])
    elif isinstance(vm.data_stack[-2], float):
        vm.data_stack[-1] = float(vm.data_stack[-1])
    else:
        if nopop:
            y = vm.data_stack[-1]
            x = vm.data_stack[-2]
        else:
            y = vm.data_stack.pop()
            x = vm.data_stack.pop()
        vm.data_stack.append(int(intop(x, y)))
        return
    if nopop:
        y = vm.data_stack[-1]
        x = vm.data_stack[-2]
    else:
        y = vm.data_stack.pop()
        x = vm.data_stack.pop()
    vm.data_stack.append(float(floatop(x, y)))

def run_block(vm, block):
    block.at = 0
    for subtok in block:
        run(vm, subtok, lambda : next(block))
    block.at = 0

def run(vm, tok, get_next, nopop=False):
    if tok.id == token.TOKEN_PRINT:
        if len(vm.data_stack) < 1:
            raise Exception("[line {}] not enough space on stack for printing".format(tok.line))
        print(vm.data_stack[-1], end="")

    elif tok.id in (token.TOKEN_INT, token.TOKEN_FLOAT, token.TOKEN_STRING):
        vm.data_stack.append(tok.item)

    elif tok.id == token.TOKEN_POP:
        if len(vm.data_stack) < 1:
            raise Exception("[line {}] not enough space on stack for popping".format(tok.line))
        vm.data_stack.pop()

    elif tok.id == token.TOKEN_COPY:
        if len(vm.data_stack) < 1:
            raise Exception("[line {}] not enough space on stack for copying".format(tok.line))
        vm.data_stack.append(vm.data_stack[-1])
        
    elif tok.id == token.TOKEN_SWAPTOP:
        if len(vm.data_stack) < 2:
            raise Exception("[line {}] not enough space on stack for swapping".format(tok.line))
        vm.data_stack[-2], vm.data_stack[-1] = vm.data_stack[-1], vm.data_stack[-2]

    elif tok.id == token.TOKEN_STACKLOG:
        vm.log()
        input()

    elif tok.id == token.TOKEN_NOPOP:
        run(vm, get_next(), get_next, True)

    elif tok.id == token.TOKEN_BLOCK:
        vm.code_stack.append(tok.item)

    elif tok.id == token.TOKEN_RUN:
        if len(vm.code_stack) < 1:
            raise Exception("[line {}] not enough space on code stack for running".format(tok.line))
        run_block(vm, vm.code_stack[-1])

    elif tok.id == token.TOKEN_EXEC:
        if len(vm.code_stack) < 1:
            raise Exception("[line {}] not enough space on code stack for execing".format(tok.line))
        run_block(vm, vm.code_stack.pop())

    elif tok.id == token.TOKEN_IF:
        if len(vm.data_stack) < 1:
            raise Exception("[line {}] need bool for if statement".format(tok.line))
        elif len(vm.code_stack) < 1:
            raise Exception("[line {}] need code to execute for if statement".format(tok.line))
        if vm.data_stack.pop():
            run_block(vm, vm.code_stack.pop())
        else:
            vm.code_stack.pop()

    elif tok.id == token.TOKEN_IFELSE:
        if len(vm.data_stack) < 1:
            raise Exception("[line {}] need bool for if-else statement".format(tok.line))
        elif len(vm.code_stack) < 2:
            raise Exception("[line {}] need code to execute for if-else statement".format(tok.line))
        if vm.data_stack.pop():
            run_block(vm, vm.code_stack[-2])
        else:
            run_block(vm, vm.code_stack[-1])
        vm.code_stack = vm.code_stack[:-2]

    elif tok.id == token.TOKEN_WHILE:
        if len(vm.code_stack) < 1:
            raise Exception("[line {}] need code to execute for while statement".format(tok.line))
        block = vm.code_stack.pop()
        run_block(vm, block)
        if len(vm.data_stack) < 1:
            raise Exception("[line {}] need bool for while statement".format(tok.line))
        while vm.data_stack.pop():
            run_block(vm, block)
            if len(vm.data_stack) < 1:
                raise Exception("[line {}] need bool for while statement".format(tok.line))

    elif tok.id == token.TOKEN_PLUS:
        if len(vm.data_stack) >= 2:
            if isinstance(vm.data_stack[-1], str) and isinstance(vm.data_stack[-2], str):
                if nopop:
                    string2 = vm.data_stack[-1]
                    string1 = vm.data_stack[-2]
                else:
                    string2 = vm.data_stack.pop()
                    string1 = vm.data_stack.pop()
                vm.data_stack.append(string1 + string2)
                return
        mathop(vm, tok, int.__add__, float.__add__, nopop)
    elif tok.id == token.TOKEN_MINUS:
        mathop(vm, tok, int.__sub__, float.__sub__, nopop)
    elif tok.id == token.TOKEN_MULTIPLY:
        if len(vm.data_stack) >= 2:
            if isinstance(vm.data_stack[-1], str) ^ isinstance(vm.data_stack[-2], str) and\
               isinstance(vm.data_stack[-1], int) ^ isinstance(vm.data_stack[-2], int):
                if nopop:
                    string = vm.data_stack[-1]
                    number = vm.data_stack[-2]
                else:
                    string = vm.data_stack.pop()
                    number = vm.data_stack.pop()
                vm.data_stack.append(number * string)
                return
        mathop(vm, tok, int.__mul__, float.__mul__, nopop)
    elif tok.id == token.TOKEN_DIVIDE:
        mathop(vm, tok, float.__div__, float.__div__), nopop
    elif tok.id == token.TOKEN_GREATER:
        mathop(vm, tok, int.__gt__, float.__gt__, nopop)
    elif tok.id == token.TOKEN_GTE:
        mathop(vm, tok, int.__ge__, float.__ge__, nopop)
    elif tok.id == token.TOKEN_LESS:
        mathop(vm, tok, int.__lt__, float.__lt__, nopop)
    elif tok.id == token.TOKEN_EQUALS:
        if len(vm.data_stack) < 2:
            raise Exception("[line {}] need two items for equality test".format(tok.line))
        if nopop:
            x = vm.data_stack[-1]
            y = vm.data_stack[-2]
        else:
            x = vm.data_stack.pop()
            y = vm.data_stack.pop()
        vm.data_stack.append(int(x == y))

    elif tok.id == token.TOKEN_WORD_DECL:
        word = get_next()
        if word.id != token.TOKEN_WORD:
            raise Exception("[line {}] excepted word name after 'word' keyword".format(tok.line))
        if len(vm.code_stack) < 1:
            raise Exception("[line {}] need code block to assign word".format(tok.line))
        vm.words[word.item] = vm.code_stack.pop()

    elif tok.id == token.TOKEN_WORD:
        block = deepcopy(vm.words.get(tok.item, "0"))()
        if block == "0": # words can't be number literals
            raise Exception("[line {}] cannot find word '{}'".format(tok.item))
        run_block(vm, block)