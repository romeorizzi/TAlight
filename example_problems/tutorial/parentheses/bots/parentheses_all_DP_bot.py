#!/usr/bin/env python3
from sys import argv, stdout, stderr

MAX_N_PAIRS = 1000

# num_wffs[num_pairs] = number of well-formed formula with <num_pairs> open parentheses and <num_pairs> closed parentheses correctly matching with them.

num_wffs = [1] * (MAX_N_PAIRS+1) # while allocating w also set up the correct value for the two base cases

for num_pairs in range(2,MAX_N_PAIRS+1):
    num_wffs[num_pairs] = 0
    for n_pairs_included in range(num_pairs):
        num_wffs[num_pairs] += num_wffs[n_pairs_included] * num_wffs[num_pairs - n_pairs_included -1] 

def num_sol(num_pairs):
    assert num_pairs <= MAX_N_PAIRS
    return num_wffs[num_pairs]

def unrank(n_pairs, pos, sorting_criterion="loves_opening_par"):
    if n_pairs == 0:
        return ""
    """(  ... )  ...
           A      B
    """    
    count = 0
    for n_pairs_in_A in range(n_pairs) if sorting_criterion=="loves_closing_par" else reversed(range(n_pairs)):
        num_A = num_sol(n_pairs_in_A)
        num_B = num_sol(n_pairs - n_pairs_in_A -1)
        if count + num_A*num_B > pos:
            break
        count += num_A*num_B
    return "(" + unrank(n_pairs_in_A, (pos-count) // num_B, sorting_criterion) + ")" + unrank(n_pairs - n_pairs_in_A -1, (pos-count) % num_B, sorting_criterion)

def rank(wff, sorting_criterion="loves_opening_par"):
    if wff == "":
        return 0
    num_dangling_open = 0
    for char, i in zip(wff,range(len(wff))):
        if char == '(':
            num_dangling_open += 1
        else:
            num_dangling_open -= 1
            if num_dangling_open == 0:
                break
    assert  i%2 == 1
    """
       (  ... )  ...    with len(A) even
       0   A  i    B
    """
    n_pairs = len(wff)//2
    count = 0
    if sorting_criterion=="loves_opening_par":
        for ii in range(i+2, len(wff)+1, 2):
            n_pairs_A = ii//2
            n_pairs_B = n_pairs - n_pairs_A -1
            num_A = num_sol(n_pairs_A)
            num_B = num_sol(n_pairs_B)
            count += num_A*num_B
    if sorting_criterion=="loves_closing_par":
        for ii in range(1, i-1, 2):
            n_pairs_A = ii//2
            n_pairs_B = n_pairs - n_pairs_A -1
            num_A = num_sol(n_pairs_A)
            num_B = num_sol(n_pairs_B)
            count += num_A*num_B
    n_pairs_A = i//2
    n_pairs_B = n_pairs - n_pairs_A -1
    num_B = num_sol(n_pairs_B)
    return count + rank(wff[1:i], sorting_criterion)*num_B + rank(wff[i+1:len(wff)+1], sorting_criterion)

def lista(n_tiles, sort_crit):
    solu=[]
    for i in range (num_sol(int(n_tiles))):
        solu.append(unrank(int(n_tiles),i,sort_crit))
    return solu

def next_wff(wff):
    n_pairs = len(wff) // 2
    r = rank(wff)
    assert r < num_sol(n_pairs) -1
    return unrank(n_pairs, r+1)


def num_sol_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(num_sol(int(tmp)))

def unrank_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            n, r = map(int, tmp.split())
            print(unrank(n, r))

def rank_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(rank(tmp))

def next_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            print(next_wff(tmp))

def list_bot():
    while True:
        tmp = input()
        if len(tmp) == 0 or tmp[0] != '#':
            n_tiles, sort_crit = map(str, tmp.split())
            print(' , '.join(lista(n_tiles, sort_crit)))

usage=f"""I am a general (non efficient) purpouse bot with the following functionalities:
  1. num_sol
  2. rank
  3. unrank
  4. next
  5. list
You should call me as follows:
$ {argv[0]} <evalution service>
"""
if len(argv) != 2:
    print(f"ERROR from bot {argv[0]}: called with the wrong number of parameters.")
    print(usage)
    exit(1)
if argv[1] == 'num_sol':
    num_sol_bot()
if argv[1] == 'rank':
    rank_bot()
if argv[1] == 'unrank':
    unrank_bot()
if argv[1] == 'next':
    next_bot()
if argv[1] == 'list':
    list_bot()