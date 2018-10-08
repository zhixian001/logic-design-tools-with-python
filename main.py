# -*- coding: utf-8 -*-
# author: JH Yeom

import sys
import parse_json
import truthtable_gen
import os
import time


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

HELP="Help\n\
help:\t show this message\n\
exit:\t exit program\n\
quit:\t exit program\n\
json:\t make truth table using 'input.json' file's data\n\
clear:\t clear this window\n\
\n\n\
not A\n\
    \A\n\
    ~A\n\
    !A\n\n\
A and B \n\
    A * B\n\
    A & B\n\n\
A or B\n\
    A + B\n\
    A | B\n\n\
A nand B\n\
    A # B\n\n\
A nor B\n\
    A @ B\n\n\
A xor B\n\
    A ^ B\n\n\
A xnor B\n\
    A = B\n\n"


if __name__ == "__main__":
    if "win" in sys.platform:
        SYSTEM_TYPE = "win"
    elif "linux" in sys.platform:
        SYSTEM_TYPE = "linux"
    else:
        SYSTEM_TYPE = "unknown"

    sys.stdout.write("\n\nTruth Table Generator by JHYeom.\n\n")
    sys.stdout.write(MANUAL)
    sys.stdout.write("\nIf you want to quit. Type 'exit', 'quit' or Press Ctrl+C.\n")
    sys.stdout.write("\nIf you want to do json jobs, type 'json'\n")
    sys.stdout.write("\nUnfortunately I handled Few Exceptions, so please use carefully!\n")
    while True:
        sys.stdout.write("\nType command or boolean expression > ")
        exp = sys.stdin.readline()
        exp = exp.replace("\n", "")
        exp = exp.replace("\r", "")
        if exp == "quit":
            sys.exit(0)
        elif exp == "exit":
            sys.exit(0)
        elif exp == "help":
            sys.stdout.write(HELP)
        elif exp == "json":
            sys.stdout.write("JSON Working...\n")
            jbool = truthtable_gen.DrawTT()
            jbool.load_exp_from_json()
            try:
                jbool.gen_tt()
                jbool.make_csv()
            except IndexError as e1:
                print("\nIndexError. There's Something problem with your json or this program.\n")
                continue
            except PermissionError as e2:
                print("\nPermissionError. Close CSV file to write!\n")
                continue
        elif exp == "clear":
            if SYSTEM_TYPE == "win":
                os.system('cls')
            elif SYSTEM_TYPE == "linux":
                os.system("clear")
        else:
            sys.stdout.write(exp)
            sys.stdout.write("\n")
            now_filename = time.strftime("%Y%m%d-%H%M%S")
            
            try:
                syms = truthtable_gen.DrawTT.parse_inputs(exp)
                nlist = truthtable_gen.DrawTT._ttable(exp, syms, [])
                with open (os.path.join("output", now_filename+".csv"), mode='w') as f:
                    f.write(exp)
                    f.write(',')
                    for sym in syms:
                        f.write(sym)
                        f.write(',')
                    f.write("Out")
                    f.write("\n")

                    for n_list_index in range(len(nlist)):
                        f.write(str(n_list_index))
                        f.write(',')
                        for in_n in range(len(syms)):
                            f.write(str(nlist[n_list_index][in_n]))
                            f.write(',')
                        f.write(str(nlist[n_list_index][-1]))
                        f.write('\n')
            except IndexError as e3:
                print("\nIndexError. There's Something problem with your expression or this program.\n")
                continue
            except PermissionError as e4:
                print("\nPermissionError. Close CSV file to write!\n")
                continue
            else:
                t = "Check " + now_filename + "\n"
                sys.stdout.write(t)






