# -*- coding: utf-8 -*-
# author: JH Yeom


import re
import sys
import os.path as ospath
import os
import parse_json

# TODO: Check invalid symbols and expressions with re

class DrawTT(object):
    def __init__(self, expression=None):
        self.json_data = []
        exps=[]
        if expression != None:
            exps.append(expression)
    
    def load_exp_from_json(self, filename="input.json"):
        json_data = parse_json.Boolexp(filename)
        for d in json_data.yield_exp():
            self.json_data.append(d)

    def _expand_doncares(self):
        for i in range(len(self.json_data)):
            dontcares = self.json_data[i][1]['dont-cares']
            new_dontcares = []
            for d in dontcares:
                occurance = d.count("*")
                if occurance == 0:
                    new_dontcares.append(d)
                else:
                    temp = [d]
                    for i in range(occurance):
                        temp2 = []
                        for rep in temp:
                            temp2.append(rep.replace("*", "1", 1))
                            temp2.append(rep.replace("*", "0", 1))
                        temp = temp2[:]
                    new_dontcares.extend(temp)
            self.json_data[i][1]['dont-cares'] = new_dontcares[:]

    def _parse_inputs(self, expression=None):
        special_op_re = re.compile("[^\~!\'\\*&+|#@^=><()]*[0-9A-Za-z]{1,2}[^\~!\'\\*&+|#@^=><()]*")
        for i in range(len(self.json_data)):
            self.json_data[i][1]['expression'] = self.json_data[i][1]['expression'].replace(" ", "")
            symbols = list(set(re.findall(special_op_re, self.json_data[i][1]['expression'])))
            for invisible in self.json_data[i][1]["not-shown"]:
                symbols.append(invisible)
            if self.json_data[i][1]['order'] == 0:
                symbols.sort(reverse=False)
            else:
                symbols.sort(reverse=True)
            self.json_data[i][1]['symbols'] = symbols
            self._expand_doncares()

    @staticmethod
    def parse_inputs(expression):
        special_op_re = re.compile("[^\~!\'\\*&+|#@^=><()]*[0-9A-Za-z]{1,2}[^\~!\'\\*&+|#@^=><()]*")
        new_exp = expression.replace(" ", "")
        syms = list(set(re.findall(special_op_re, new_exp)))
        syms.sort()
        return syms

    def gen_tt(self):
        self._parse_inputs()
        for i in range(len(self.json_data)):
            self.json_data[i][1]['ttable'] = self._ttable(self.json_data[i][1]['expression'], self.json_data[i][1]['symbols'], self.json_data[i][1]['dont-cares'])

    def make_csv(self):
        # TODO: Check output dir and if not exist, create.
        if "output" not in os.listdir(os.getcwd()):
            os.mkdir(ospath.join(os.getcwd(), "output"))
        for i in range(len(self.json_data)):
            with open(ospath.join("output", self.json_data[i][0]+".csv"), mode='w') as f:
                f.write(self.json_data[i][1]['expression'])
                f.write(',')
                for sym in self.json_data[i][1]['symbols']:
                    f.write(sym)
                    f.write(',')
                f.write(self.json_data[i][0])
                f.write("\n")

                for n_list_index in range(len(self.json_data[i][1]['ttable'])):
                    f.write(str(n_list_index))
                    f.write(',')
                    for in_n in range(len(self.json_data[i][1]['symbols'])):
                        f.write(str(self.json_data[i][1]['ttable'][n_list_index][in_n]))
                        f.write(',')
                    f.write(str(self.json_data[i][1]['ttable'][n_list_index][-1]))
                    f.write('\n')
            sys.stdout.write("Created ")
            sys.stdout.write(ospath.join("output", self.json_data[i][0]+".csv"))
            sys.stdout.write("\n")

    @staticmethod
    def _ttable(expression, inputs, dontcare):
        # orig_expression =expression
        n_list = []
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
                # FIXME:
                else:
                    if DrawTT._get_weight(char) > DrawTT._get_weight(stack[-1]):
                        stack.append(char)
                    else:
                        while len(stack) > 0 and DrawTT._get_weight(char) <= DrawTT._get_weight(stack[-1]):
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
            
            doncare_chkstr = ""
            for c in bin_num:
                if c == True:
                    doncare_chkstr += "1"
                else:
                    doncare_chkstr += "0"

            if doncare_chkstr in dontcare:
                """ for p in range(len(bin_num)):
                    bin_num[p] = "X" """
                bin_num.append("X")
            else:
                bin_num.append(DrawTT._calculate_postfix(new_exp, bin_num))
            print(bin_num[-1])

            n_list.append(bin_num)

        print()
        return n_list
        
    @staticmethod
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

    @staticmethod
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
    # sys.stdout.write("\n\nTruth Table Generator by JHYeom.\n\n")
    # sys.stdout.write(MANUAL)
    # sys.stdout.write("\nIf you want to quit. Press Ctrl+C\n")
    """ while True:
        sys.stdout.write("\nType boolean expression > ")
        exp = sys.stdin.readline()
        print(exp)
        exp = exp.replace("\n", "")
        try:
            ttable(exp, *_parse_inputs(exp))
        except IndexError as e1:
            print("\nIndexError. There's Something problem with your expression or this program.\n")
        except PermissionError as e2:
            print("\nPermissionError. Close CSV file to write!\n") """

    a = DrawTT()
    a.load_exp_from_json()
    a.gen_tt()
    a.make_csv()
    

        
