# -*- coding: utf-8 -*-
# author: JH Yeom

MANUAL="Symbol Support up to 2 chars\n\
You Cannot make symbol name using ['~', '!', '\'', '\\' '*', '&', '+', '|', '#', '@', '^', '=', '>', '<', '(', ')']\n\
Symbol Name should Start with Alphabet\n\
# of input symbol is currently < 10\n\
\n\
not A\n\
    \A\n\
    ~A\n\
    !A\n\
    A' : future support\n\
A and B \n\
    AB : future support\n\
    A * B\n\
    A & B\n\
A or B\n\
    A + B\n\
    A | B\n\
A nand B\n\
    A # B\n\
A nor B\n\
    A @ B\n\
A xor B\n\
    A ^ B\n\
A xnor B\n\
    A = B\n\
A implies B\n\
    A > B : future\n"

import re
import sys

# TODO: Check invalid symbols and expressions with re


def _parse_inputs(expression):
    special_op_re = re.compile("[^\~!\'\\*&+|#@^=><()]*[0-9A-Za-z]{1,2}[^\~!\'\\*&+|#@^=><()]*")
    new_exp = expression.replace(" ", "")
    syms =list(set(re.findall(special_op_re, new_exp)))
    syms.sort()
    
    return syms
    


def ttable(expression, *inputs):
    #remove spaces in expression
    expression = expression.replace(" ", "")
    # not
    expression = expression.replace("!", "~")
    expression = expression.replace("\\", "~")
    expression = expression.replace("!", "~")
    # and
    expression = expression.replace("*", "&")
    # or 
    expression = expression.replace("+", "|")

    # double negate correct
    expression = expression.replace("~~", "")

    # replace expression with its index
    for sym in inputs:
        expression = expression.replace(sym, str(inputs.index(sym)))

    # TODO: POSTFIX alg
    # convert to postfix
    stack = []
    new_exp = []
    number_re = re.compile('[0-9]')
    for char in expression:
        if number_re.match(char):
            new_exp.append(int(char))
        else:
            if len(stack) == 0:
                stack.append(char)
            elif char == "(":
                stack.append(char)
            elif char == ")":
                while True:
                    t = stack.pop()
                    if t == "(":
                        break
                    new_exp.append(t)
            # TODO: fix
            else:
                if _get_weight(char) > _get_weight(stack[-1]):
                    stack.append(char)
                else:
                    while len(stack) > 0 and _get_weight(char) <= _get_weight(stack[-1]):
                        new_exp.append(stack.pop())
                    stack.append(char)
    while len(stack) != 0:
        t = stack.pop()
        if t == "(":
            continue
        new_exp.append(t)

    # ####################

    bin_num = list(False for i in range(len(inputs)))
    print(end="\t")
    for sym in inputs:
        print(sym, end="\t")
    print("Out")
    for i in range(2**len(inputs)):
        print(i, end="\t")
        bin_num = list(False for i in range(len(inputs)))
        for j in range(len(inputs)-1, -1, -1):
            if i // 2**j == 1:
                bin_num[len(inputs) - j - 1] = True
                i -= 2**j
        for val in bin_num:
            print(val, end="\t")
        ####################
        #calculate output
        # TODO:

        print(_calculate_postfix(new_exp, bin_num))
        ####################
    

def _get_weight(oprt):
    if oprt == '&':
        return 9
    elif oprt == '|':
        return 7
    elif oprt == '(':
        return 5
    elif oprt == '~':
        return 12
    elif oprt == '^':
        return 11
    elif oprt == '=':
        return 10
    elif oprt == '#':
        return 8
    elif oprt == '@':
        return 6
    else:
        return -1

def _calculate_postfix(postfix_exp, bin_num):
    stack = []
    for char in postfix_exp:
        if type(char) == int:
            stack.append(bin_num[char])
        elif char == '~':
            t = stack.pop()
            stack.append(bool(~t&True))
        elif char == '&':
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(t1&t2)
        elif char == '|':
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(t1|t2)
        elif char == '^':
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(t1^t2)
        elif char == '#':
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(bool(~(t1&t2)&1))
        elif char == '@':
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(bool(~(t1|t2)&1))
        elif char == '=':
            t1 = stack.pop()
            t2 = stack.pop()
            stack.append(bool(~(t1^t2)&1))
    return stack.pop()


if __name__ == "__main__":
    sys.stdout.write("\n\nTruth Table Generator by JHYeom.\n\n")
    sys.stdout.write(MANUAL)
    sys.stdout.write("\nIf you want to quit. Press Ctrl+C\n")
    while True:
        sys.stdout.write("\nType boolean expression > ")
        exp = sys.stdin.readline()
        print(exp)
        exp = exp.replace("\n", "")

        ttable(exp, *_parse_inputs(exp))
        
