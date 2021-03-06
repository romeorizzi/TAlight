#!/usr/bin/env python3

import itertools
import re
import random
import time
import sys

def parse_input(string):
    string = remove_duplicate_spaces(string)
    l = list(string.split(" "))
    l = list(map(int, l))
    return l

def remove_duplicate_spaces(T):
    return re.sub(' +', ' ', T)

def is_subseq_with_position(s, T):
    pos = []
    i_T = 0
    i_s = 0
    while (i_T < len(T) and i_s < len(s)):
        if T[i_T] == s[i_s]: 
            i_s+=1
            pos.append(i_T)
        i_T +=1
    if i_s == len(s):
        return [True, pos]
    else:
        return [False, pos]

def get_yes_certificate(T, pos):
    cert = ""
    index = 0
    i = 0
    while (i < len(T) and index < len(pos)):
        num_ciphers = len(str(T[i]))        
        if i == pos[index]:
            index+=1
            for _ in range(0, num_ciphers):
                cert+= "^"
        else:
            for _ in range(0, num_ciphers):
                cert+= " " 
        cert+= " "
        i+=1
    return cert

    
def sub_sequences_num(T):
    combs = []
    seq_num = 0
    for l in range(1, len(T)+1):
        combs.append(list(itertools.combinations(T, l)))
    for c in combs:
        for t in c:
            seq_num+=1
    return seq_num

def alphabet_of(T):
    "restituisce il set dei caratteri che appaiono in T, ciascuno con la prima posizione in cui appare in T"
    alpha = {}
    for char, pos in zip(T,range(len(T))):
        if char not in alpha.keys():
            alpha[char] = pos
    return alpha
'''
def sub_sequences(T):
    """return the list of possible non-empty subsequnces of the string T
    Example: sub_sequences("AA") returns ["", "A", "AA"]
    """ 
    risp = [""]
    if len(T) == 0:
        return risp 
    alive_subseq = [("",0)]
    while len(alive_subseq) > 0:
        next_alive_subseq = []
        for s,pos in alive_subseq:
            for char, pos2 in alphabet_of(T[pos:]).items():
                pos += pos2
                new_subseq = s+char
                risp.append(new_subseq)
                if pos < len(T)-1:
                    next_alive_subseq.append((new_subseq,pos+1))
        alive_subseq = next_alive_subseq
    return risp
'''
#with duplicate
def sub_lists_with_pos (l):
    empty = []  
    lists = [empty]
    for i in range(len(l)):
        orig = lists[:]
        new = (l[i],i)
        for j in range(len(lists)):
            lists[j] = lists[j] + [new]

        lists = orig + lists
    return lists
  
def generate_random_inc_seq(length, max_val, stricty=True, seed=None):
    assert not stricty or length <= max_val +1
    if seed != None:
        random.seed(seed)
    if strictly:
        return sorted(random.sample(range(max_val+1), length))
    else:
        return sorted(random.choice(range(max_val+1), length))
    
def generate_random_dec_seq(length, max_val, stricty=True, seed=None):
    return generate_random_inc_seq(length, max_val, stricty, seed).reversed()

def get_random_subseq(T, n, seed=None):
    if seed == None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    return [T[i] for i in sorted(random.sample(range(len(T)), n)) ], seed

def generate_random_seq(length, max_val, max_incr_subseq_len=None, stricty=True, seed=None):
    """yields a random list of <length> naturals in [0, max_val].
       If seed == None then it generates a seed at random.
       In any case, it returns the seed used.""" 
    if seed == None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    T = []
    if max_incr_subseq_len==None:
        for i in range(length):
            T.append(random.randint(0,max_val))
        return T, seed
    else:
        if stricty:
            assert max_incr_subseq_len <= max_val +1
            # how we generate a random sequence whose longest increasing subsequence has length precisely max_incr_subseq_len
            # 1. we generate a random strictly increasing sequence s = s1 ... smax_incr_subseq_len
            # 2. for each i we generate a random non-increasing sequence Si containing element si
            # 3. we merge all the Si sequences taking care that the value si from Si goes before than the value s(i+1) form sequence S(i+1)
            #    But we found it more convenient to just concatenate them 

            s = generate_random_inc_seq(max_incr_subseq_len, max_val, stricty=True, seed=seed+i)
            for i in range(max_incr_subseq_len,0,-1):
                Si = generate_random_dec_seq(length//i, max_val, stricty=False, seed=seed)
                length -= len(Si)
                pos = 0
                while Si[pos] < s[i]:
                    pos += 1
                Si[pos] = s[i]
                T.append(Si)
        else:
            assert length <= max_incr_subseq_len * max_val
            # how we generate a random sequence whose longest non-decreasing subsequence has length precisely max_incr_subseq_len
            # 1. we generate a random non-decreasing sequence s = s1 ... smax_incr_subseq_len
            # 2. for each i we generate a random stricty decreasing sequence Si containing element si
            # 3. we just concatenate them 
            s = generate_random_inc_seq(max_incr_subseq_len, max_val, stricty=False, seed=seed+i)
            for i in range(max_incr_subseq_len,0,-1):
                Si = generate_random_dec_seq(length//i, max_val, stricty=True, seed=seed)
                length -= len(Si)
                pos = 0
                while Si[pos] < s[i]:
                    pos += 1
                Si[pos] = s[i]
                T.append(Si)            
    return T, seed

def gen_seq_avoiding_(s, m, max_val, seed=None):
    if seed == None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    T = []
    seen = 0
    while len(T) < m:
        if seen < len(s) -1:
            T.append(random.randint(0,max_val))
            if T[-1] == s[seen]:
                seen += 1
        else:
            T.append(random.randint(0,max_val-1))
            if T[-1] >= s[-1]:
                T[-1] += 1
    return T, seed
    
def gen_subseq_instance(m, n, max_val, yes_instance, seed=None):
    """yields an instance for the subseq decision problem.
       Both the text T (of lenght m) and the candidate subsequence s (of length n) are made of naturals in [0, max_val].
       If seed == None then it generates a seed at random.
       In any case, it returns the seed used."""
    if seed == None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    if yes_instance:
        T,_ = generate_random_seq(m, max_val, seed)
        s,_ = get_random_subseq(T, n, seed)
    else:
        s,_ = generate_random_seq(n, max_val, seed)
        T,_ = gen_seq_avoiding_(s, m, max_val, seed)
    return T, s, seed


def get_not_subseq(T, max, seed=None):
    tmp = []
    if seed != None:
        random.seed(seed)
    else:
        seed = random.randrange(sys.maxsize)
        random.seed(seed)
    tmp.append(random.randint(0, max))
    while is_subseq_with_position(tmp, T)[0]:
        tmp.append(random.randint(0, max))
    return tmp, seed
    

def get_n_subseq_all_diff(n):
    return (2**n) - 1

def LS(A , ordering):
    L = list()
    for i in range(0, len(A)):
        L.append(list())

    L[0].append(A[0])

    for i in range(1, len(A)):
        for j in range(0, i):
            if ordering == 'increasing':
                if (A[j] < A[i]) and (len(L[i]) < len(L[j])):
                    L[i] = []
                    L[i].extend(L[j])
            elif ordering == 'decreasing':
                if (A[j] > A[i]) and (len(L[i]) < len(L[j])):
                    L[i] = []
                    L[i].extend(L[j])
        L[i].append(A[i])
    return L

def find_ls(l):
    lung = 0
    index = []
    ret = []
    for i in l:
        if len(i) > lung:
            index.clear()
            lung = len(i)
            index.append(l.index(i))
        elif len(i) == lung:
            index.append(l.index(i))
    for i in index:
        if (l[i] not in ret):
            ret.append(l[i])
    return ret
   

def remove_duplicate_list(s):
    s = list(dict.fromkeys(s))
    return s

def strictly_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))

def strictly_decreasing(L):
    return all(x>y for x, y in zip(L, L[1:]))

def non_increasing(L):
    return all(x>=y for x, y in zip(L, L[1:]))

def non_decreasing(L):
    return all(x<=y for x, y in zip(L, L[1:]))
 

def check_no_ordered_list_cert(S, a, b, ordering):
    if ordering == 'not_increasing' or ordering == 'increasing':
        if S[a] >= S[b]:
            return True
        else:
            return False
    elif ordering == 'not_decreasing' or ordering == 'decreasing':
        if S[a] <= S[b]:
            return True
        else:
            return False

def min_decreasing_col(arr):
    n = len(arr)
    mdc = [1]*n
 
    for i in range (1 , n):
        for j in range(0 , i):
            if arr[i] > arr[j] and mdc[i]< mdc[j] + 1 :
                mdc[i] = mdc[j]+1
 
    return mdc

def remove_values_from_list(l, val):
   return [value for value in l if value != val]

def get_min_coloring(lis):
    maximum = max(lis)
    index_max = lis.index(maximum)
    color = [0]*len(lis)
    color_id = 1
    n_assign = 1
    first = True
    while 0 in color:
        if lis[index_max] > 0:
            #print(lis)
            
            color[index_max] = color_id
            last_index = lis[index_max]
            #print(last_index)
            lis[index_max] = 0
            
            tmp = lis[:index_max]
            print(last_index, index_max, color_id , lis ,tmp)
            #print(tmp, lis)
            tmp2 = remove_values_from_list(tmp, 0)
            if not tmp2 or  all(v >= last_index for v in tmp2) or not tmp:
                color_id+=1
                maximum = max(lis) 
                id_tmp = 0
                for i in range(0, len(lis)):
                    if lis[i] == maximum:
                        id_tmp = i
                index_max = id_tmp
                n_assign = 1
                
            else:
                maximum_tmp = max(tmp)
                #print(maximum, maximum_tmp)
                index_max_tmp = tmp.index(maximum_tmp)
                while maximum_tmp == maximum:
                    tmp[index_max_tmp] = 0
                    maximum_tmp = max(tmp)
                    for i in range(0, len(tmp)):
                        if tmp[i] == maximum_tmp:
                            index_max_tmp = i
                    index_max_tmp = tmp.index(maximum_tmp)
                
                maximum = maximum_tmp

                for i in range(0, len(tmp)):
                        if tmp[i] == maximum:
                            id_tmp = i
                
                index_max = id_tmp
                n_assign+=1
                
        
    return color


def get_max_increasing_subseq_by_color(T, color):
    n_color = max(color)
    max_n = 0
    max_sub = 0
    for i in range(1, n_color):
        tmp = color.count(i)
        if tmp > max_n:
            max_n = tmp
            max_sub = color[i]

    pos = []
    for i in range(0, len(T)):
        if color[i] == max_sub:
            pos.append(i)
    return pos


def list_to_string(T):
    string = ""
    for i in range(0, len(T)):
        string += str(T[i])
        if i != len(T) -1 :
            string +=" "
    return string


def n_coloring(color):
    return len(set(color))


def sub_sequences_list(T):
    sub_seq = []
    combs = []
    for l in range(1, len(T)+1):
        combs.append(list(itertools.combinations(T, l)))
    for c in combs:
        for t in c:
            seq = []
            for i in t:
                seq.append(i)
            sub_seq.append(seq)
    return sub_seq  #list of string


def ordered_sub_sequences(T):
    tmp = sub_sequences_list(T)
    tmp = remove_duplicate_list_of_list(tmp)
    tmp.sort()
    return tmp

def remove_duplicate_list_of_list(li):
    li = set(map(tuple,li))
    li = list(map(list, li))
    return li

def get_missing_subsequences(tot, input):
    #tot and input are list of lists
    missing = []
    for i in tot:
        if not i in input:
            missing.append(i)

    return missing


import math

def get_prefix(s):
    return s[:math.floor(len(s)/2)]

def get_position_from_subseq(subseq, all_subseq):
    index_subseq = []
    
    for i in all_subseq:
        if i:
            c,v = zip(*i)
            if subseq == list(c):
                index_subseq.append(list(v))

    return index_subseq

def get_input_with_time(regexp=None):
    ok = True
    start = time.time()
    user_input = input()
    end = time.time()
    elapsed = end - start
    if regexp!=None:
        ok = bool(re.match(regexp, user_input))
    return user_input, elapsed, ok

def get_growth_rate(previous, current):
    return current/previous


#return n seed
def list_of_seed(seed,n):
    if seed == None:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    seeds = []
    for i in range(n):
        seeds.append(random.randrange(sys.maxsize))
    return seed, seeds


def count_increasing_sub(arr, n, max_val):
    count = [0 for i in range(max_val + 1)]

    for i in range(n):
        for j in range(arr[i] - 1, -1, -1):
            count[arr[i]] += count[j]

        count[arr[i]] += 1

    result = 0
    for i in range(max_val + 1):
        result += count[i]

    return result


def count_occurences(T, S):
    m = len(T) #T
    n = len(S)  #S

    lookup = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(n + 1):
        lookup[0][i] = 0

    for i in range(m + 1):
        lookup[i][0] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if T[i - 1] == S[j - 1]:
                lookup[i][j] = lookup[i - 1][j - 1] + lookup[i - 1][j]
            else:
                lookup[i][j] = lookup[i - 1][j]

    return lookup[m][n]

def get_max_inc_seq(T,col):
    max_col = max(col)
    T_tmp = T[:]
    ret = []
    for i in range(len(T)-1, -1, -1):
        if col[i] == max_col:
            ret.append(T[i])
            max_col = max_col-1

    ret.reverse()
    return ret

def CeilIndex(A, l, r, key):
    while (r - l > 1):
        m = l + (r - l)//2
        if (A[m] >= key):
            r = m
        else:
            l = m
    return r
  
def LongestIncreasingSubsequenceLength(A, size):
    tailTable = [0 for i in range(size + 1)]
    length = 0
    tailTable[0] = A[0]
    length = 1
    for i in range(1, size):
     
        if (A[i] < tailTable[0]):
            tailTable[0] = A[i]
  
        elif (A[i] > tailTable[length-1]):
            tailTable[length] = A[i]
            length+= 1
        else:
            tailTable[CeilIndex(tailTable, -1, length-1, A[i])] = A[i]
         
    tailTable = tailTable[:length]
    return tailTable, length
