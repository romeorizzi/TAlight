#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="sum"
service="sum"
args_list = [
    ('num_questions',int),
    ('numbers',str),
    ('obj',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
from random import randrange

from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

gen_new_s = True    
for _ in range(ENV['num_questions']):
    if gen_new_s:
        if ENV['numbers'] == "onedigit":
            s = randrange(10)
        elif ENV['numbers'] == "twodigits":
            s = randrange(100)
        else:
            s = randrange(2**64)
    TAc.print(f"? {s}", "yellow", ["bold"])
    spoon = input().strip()
    if spoon=='':
        gen_new_s = False
        TAc.NO() 
        TAc.print(LANG.render_feedback("wrong-input-two", f"Attenzione non hai inserito alcun numero"), "red", ["underline"])
    else:
        while spoon[0] == '#':
            spoon = input().strip()
        if spoon.count(' ')==0:
            gen_new_s = False
            TAc.NO() 
            TAc.print(LANG.render_feedback("wrong-input", f"L'input che hai inserito non è del formato corretto, dovresti inserire due numeri separati da uno spazio"), "red", ["underline"])
        else:
            a, b = map(int, spoon.split(" "))
            gen_new_s = False
            if a+b > s:
                TAc.NO() 
                TAc.print(LANG.render_feedback("too-much", f"indeed, {a}+{b}={a+b} > {s}."), "yellow", ["underline"])        
            elif a+b < s:
                TAc.NO() 
                TAc.print(LANG.render_feedback("too-little", f"indeed, {a}+{b}={a+b} < {s}."), "yellow", ["underline"])        
            else: # a + b == n
                if ENV['obj'] == "max_product":
                    if a < b:
                        a,b = b,a
                    if a-b > 1:
                        TAc.NO() 
                        TAc.print(LANG.render_feedback("not-balanced", f"indeed, {a-1}+{b+1}={s} and {a-1}*{b+1}={(a-1)*(b+1)} > {a*b}={a}*{b}."), "yellow", ["underline"])        
                    else:
                        gen_new_s = True
                        TAc.OK()
                        TAc.print(LANG.render_feedback("max-product", f"indeed, x={a} and y={b} have maximum product among the integer numbers with x+y={s}. Do you know why? Do you have a proof for your intuition?"), "grey")
                else:
                    TAc.OK()
                    TAc.print(LANG.render_feedback("right-sum", f"indeed, {a}+{b}={s}"), "grey")        
                    gen_new_s = True
            
TAc.Finished()
exit(0)