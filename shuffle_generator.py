import os

import json
import shutil

import words as wd
import shuffle as sh

from shuffles_analizer import retrieve_json_data

def generate_increasing_words(alph, lim_sup, lim_inf=0):
    """
    Generator which takes an ordered alphabet
    and yields words in lexicographic order.
    It starts in alph[0]^lim_inf and ends 
    before surpassing length lim_sup.
    """
    current = ""
    for i in range(lim_inf):
        current = alph[0]+current
    while(len(current)<=lim_sup):
        yield current
        current = wd.next_lex(current,alph)

def generate_increasing_words_up_to(alph, final_w, init_w=""):
    """
    Generator which takes:
    * an ordered alphabet
    * an initial word init_w
    * a final word final_w
    and yields in lexicographical order all words between them,
    including them.

    If init_w is not specified, it starts with "alph[0]".
    """
    current = init_w if init_w != "" else alph[0]
    while wd.is_lesser_or_equal_lex(current,final_w,alph):
        yield current
        current = wd.next_lex(current,alph)

def generate_canonical_words(alph, lim_sup, lim_inf=0):
    """
    Generator which takes an ordered alphabet and
    yields all canonical words in a range, in
    "roughly" lexicographic order.
    It starts in alph[0]^lim_inf and ends 
    before surpassing length lim_sup.

    It REQUIRES |alph|>1.
    Otherwise it's very easy to do and I don't
    want to spend time accounting for that case.
    """
    for n in range(lim_inf, lim_sup+1):
        pivot = alph[0]
        for w in generate_canonical_words_recursively(alph,pivot,n):
            yield w

def generate_canonical_words_recursively(alph,pivot,n):
    """
    Generates all possible words of length n 
    which start with "pivot" and does so in a 
    "roughly" lexicographic order of the alphabet.

    This is an auxiliary function to
    "generate_canonical_words"
    """ 
    if pivot in alph:
        for m in range(n,0,-1):
            pivots = wd.enlengthen(pivot,m)
            if m==n:
                yield pivots
            else:
                pivot_index = alph.find(pivot)
                new_pivot_index = pivot_index+1
                new_pivot = alph[new_pivot_index] if new_pivot_index<len(alph) else alph+"0"
                # this is designed so that (new_pivot in alph) is false whenever new_pivot_index exceeds len(alph)
                for w in generate_canonical_words_recursively(alph,new_pivot,n-m):
                    yield pivots+w
    else:
        init_w = wd.enlengthen(alph[0],n)
        final_w = alph[-2]+wd.enlengthen(alph[-1],n-1)
        for w in generate_increasing_words_up_to(alph,final_w,init_w):
            yield w

def generate_words_from_parikh(alph,p):
    """
    A generator which yields ALL possible words
    comprised by the symbols in a given Parikh vector.
    """
    s = sum(p)
    if s==0:
        yield ""
    else:
        for c in alph:
            i = alph.find(c)
            if p[i]>0:
                new_p = p.copy()
                new_p[i] = new_p[i]-1
                for w in generate_words_from_parikh(alph,new_p):
                    yield c+w


def generate_canonical_words_from_parikh(alph,p):
    """
    A generator which yields all possible CANONICAL
    words comprised by the symbols in a given
    Parikh vector.

    It REQUIRES the truthfulness of (wd.is_canonical_parikh(p))
    """
    n = p.index(0) if 0 in p else len(p)
    new_alph = alph[:n]
    new_p = p[:n]
    for w in generate_canonical_words_from_parikh_recursively(new_alph,new_p):
        yield w

def generate_canonical_words_from_parikh_recursively(alph,p,pivot=0):
    """
    An auxiliary function for generate_canonical_words_from_parikh.
    It takes the corrected alphabet and parikh vectors
    (because of the canonicity hypothesis on p, it can be assumed
    that it has an irrelevant tail of zeroes).

    It adds characters in the correct order to guarantee canonicity,
    and then makes use of generate_words_from_parikh to build the
    word's tail.
    """
    if sum(p)==0:
        yield ""
    elif pivot>=len(p):
        for i in range(len(p)-1):
            if p[i]>0:
                new_p = p.copy()
                new_p[i] = new_p[i]-1
                for w in generate_words_from_parikh(alph,new_p):
                    yield alph[i]+w
    else:
        for keep in range(p[pivot],0,-1):
            new_p = p.copy()
            new_p[pivot] = new_p[pivot]-keep
            pivots = wd.enlengthen(alph[pivot],keep)
            for w in generate_canonical_words_from_parikh_recursively(alph,new_p,pivot=pivot+1):
                yield pivots+w


def to_dict(w1,w2,w3,l,m,b):
    data = {
        'w1': w1,
        'w2': w2,
        'w3': w3,
        'ways_to_shuffle':l,
        'ways_to_commute':m,
        'commuting_is_enough':b
    }
    return data

def to_json(w1,w2,w3,l,m,b):
    d = to_dict(w1,w2,w3,l,m,b)
    json_str = json.dumps(d,indent=2)
    return json_str

def generate_shuffles_to_file(alph,N):
    """
    Given an ordered alphabet <alph> and a natural number <N>, it generates a json file
    containing all tuples (w1,w2,w3) such that:
    * w1,w2,w3 are words on <alph>
    * w1 and w2 can be shuffled to obtain w3
    * w1 is always lexicographically smaller than w2 for the order in <alph>
    * w3 is always a canonical word on <alph> (that is, its first letter to appear is always alph[0], the second alph[1], etc.)
    The last two points are there to avoid obvious duplicates in the file.
    
    The file contains the number of ways w1 and w2 can be shuffled to obtain w3,
    and also whether simple commutations from a single shuffle are enough to obtain all
    possible shuffles.

    The results are written to file <shuffle_to_N_alph> in the same folder from where
    this script is run. 
    """
    filename = "shuffles_to_"+str(N)+"_"+alph

    first_time = True
    lenw1 = 1

    with open(filename,'w') as file:
        print("Starting to generate shuffles.")
        file.write('[')
        gen1 = generate_increasing_words(alph,N,lim_inf=1)
        for w1 in gen1:
            if len(w1)>lenw1:
                print(f"Generating words of length {len(w1)} for w1.")
                lenw1=len(w1)
            last_symbols = wd.enlengthen(alph[-1],N-1)
            if w1[0] != alph[0]:
                gen2 = generate_increasing_words_up_to(alph,alph[0]+last_symbols,init_w=w1)
                #w3 will be canonical, so if w1 does not start with alph[0] then w2 does
                #maybe there's a way to generalize this to also guarantee parikh(w1+w2) is canonical-parikh?
            else:    
                gen2 = generate_increasing_words_up_to(alph,alph[-1]+last_symbols,init_w=w1)
            for w2 in gen2:
                p = wd.word_to_parikh(w1+w2,alph)
                if not wd.is_canonical_parikh(p):
                    continue
                gen3 = generate_canonical_words_from_parikh(alph,p) #remember that this requires wd.is_canonical_parikh(p)
                for w3 in gen3:
                    try:
                        L = sh.all_possible_shuffles(w1,w2,w3,alph=alph)
                        l = len(L)
                        try:
                            S = L[0]
                            M = sh.all_possible_commutations(S)
                            m = len(M)
                            b = sh.compare_sets_of_shuffles(L,M)
                            s = to_json(w1,w2,w3,l,m,b)
                            if first_time:
                                file.write("\n")
                                first_time=False
                            else:
                                file.write(",\n")
                            file.write(s)
                        except IndexError:
                            #print(f"{w1},{w2} cannot be shuffled into {w3}")
                            continue
                    except sh.ShuffleError as err:
                        #print(err)
                        continue  
        file.write('\n]')
        print("Generation complete.") 

def add_shuffles_and_append(filename,alph,n,N):
    """
    Auxiliary function to complete shuffle files up to 
    an N>n input size.

    Despite its name, a new file is generated where 
    the whole thing is dumped.
    """
    new_filename = "shuffles_to_"+str(N)+"_"+alph

    shutil.copy(filename, new_filename)

    with open(new_filename,'rb+') as file:
        file.seek(-2,os.SEEK_END)
        file.truncate()

    first_time = True
    lenw1 = 1

    print(f"Writing on new file {new_filename}...")
    with open(new_filename,'a') as file:
        file.write(",\n")
        print("Starting to generate shuffles.")
        
        gen1 = generate_increasing_words(alph,N,lim_inf=1)
        for w1 in gen1:
            if len(w1)>lenw1:
                print(f"Generating words of length {len(w1)} for w1.")
                lenw1=len(w1)
            N_word = wd.enlengthen(alph[-1],N)
            n_word = wd.enlengthen(alph[0],n+1)
            min_word = n_word if wd.is_greater_lex(n_word,w1,alph) else w1  
            gen2 = generate_increasing_words_up_to(alph,N_word,init_w=min_word)
            for w2 in gen2:
                p = wd.word_to_parikh(w1+w2,alph)
                if not wd.is_canonical_parikh(p):
                    continue
                gen3 = generate_canonical_words_from_parikh(alph,p)
                for w3 in gen3:
                    try:
                        L = sh.all_possible_shuffles(w1,w2,w3,alph=alph)
                        l = len(L)
                        try:
                            S = L[0]
                            M = sh.all_possible_commutations(S)
                            m = len(M)
                            b = sh.compare_sets_of_shuffles(L,M)
                            json_str = to_json(w1,w2,w3,l,m,b)
                            if first_time:
                                first_time=False
                            else:
                                file.write(",\n")
                            file.write(json_str)                            
                        except IndexError:
                            #print(f"{w1},{w2} cannot be shuffled into {w3}")
                            continue
                    except sh.ShuffleError:
                        continue
        file.write("\n]")
        print("Generation complete.")

def complete_ways_to_commute_in_thing(thing,rule):
    """
    Completes the "way_to_commute" parameter in a given thing
    by using a particular rule of commutation.
    The rule must be a function which returns a list of all
    possible "commutations" of a shuffle, for a given criteria
    of what a commutation is.
    """
    w1 = thing["w1"]
    w2 = thing["w2"]
    w3 = thing["w3"]
    l  = thing["ways_to_shuffle"]
    b  = thing["commuting_is_enough"]

    to_visit = sh.all_possible_shuffles(w1,w2,w3)
    ways_to_commute = []
    while(len(to_visit)>0):
        S = to_visit.pop()
        comm = rule(S)
        ways_to_commute.append(len(comm))
        for T in comm:
            if T in to_visit:
                to_visit.remove(T)
    
    new_thing = to_json(w1,w2,w3,l,ways_to_commute,b)
    return new_thing

def complete_ways_to_commute_in_file(filename):
    """
    Takes the <filename> of an existing json file, and completes
    the "ways_to_commute" variable of each single shuffle entry
    to a complete description of the equivalence classes under
    simple commutativity.
    """
    new_filename = filename+"_complete_class"
    with open(new_filename,"w") as file:
        file.write('[')
        first_time = True
        for thing in retrieve_json_data(filename):
            try:
                new_thing = complete_ways_to_commute_in_thing(thing,sh.all_possible_commutations)
                if first_time:
                    file.write("\n")
                    first_time = False
                else:
                    file.write(",\n")
                file.write(new_thing)
            except BaseException:
                continue
        file.write('\n]')

def append_files(filename1,filename2,new_filename):
    """
    Auxiliary function to append two different shuffle files.
    """
    pass

def delete_duplicates(filename):
    """
    Auxiliary function to delete duplicates from already generated shuffle files.
    This is necessary because a previous version of generate_shuffles_to_file 
    generated both (w1,w2,w3) and (w2,w1,w3) separately for each pair of words w1,w2.
    """
    pass

def main(alph,N):
    generate_shuffles_to_file(alph,N)