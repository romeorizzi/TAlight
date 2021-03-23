#!/usr/bin/env python3
from sys import stderr, exit, argv
import re
import random

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from increasing_subsequence_lib import list_to_string, parse_input, generate_random_seq, get_rand_subseq, get_not_subseq, is_subseq_with_position, remove_duplicate_spaces

# METADATA OF THIS TAL_SERVICE:
problem="increasing_subseq"
service="is_subseq_server"
args_list = [
    ('times',str),
    ('lang',str),
]
ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#if not ENV['silent']:
#    TAc.print(LANG.opening_msg, "green")

string_T = ""
string_s = ""
length = int(ENV["times"])
TAc.print("\nIn this problem you are given a sequence of numbers T. You are asked to evaluate whether a sub-sequence s is part of T "+str(length)+" times. \nAnswer \"y\" if you think s is a subsequence you T, \"n\" otherwise.", "green")
string_T = generate_random_seq(10, 100)
TAc.print(list_to_string(string_T), "green")

for i in range(0, length):
    x = random.randint(1,10)
    if i == 0 or x % 2 == 0:
        string_s = get_rand_subseq(string_T)
    else:
        string_s = get_not_subseq(string_T, string_s, 100)
    TAc.print(list_to_string(string_s),"green")
    res = input()

    if res == "y" or res == "Y": 
        res = True
    elif res =="n" or res == "N":
        res = False
    else: 
        TAc.print("WRONG INPUT FORMAT: only \"y\" or \"n\" are allowed as answer.","red")
        exit(0)
    ret = is_subseq_with_position(string_s,string_T)
    if ret[0] == res:
        TAc.print("OK, your answer is correct!.\n\n","green")
    else:
        TAc.print("NO, your answer isn't correct.\n\n","red")




