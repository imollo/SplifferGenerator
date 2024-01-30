import json

import shuffle as sh
import words as wd


alph = "ab"
N = 1

def generate_increasing_words(alph, lim_sup, lim_inf=0):
    """
    Generator which takes an ordered alphabet
    and yields words in lexicographic order.
    It starts in alph[0]^lim_inf and ends 
    before reaching length lim_sup.
    """
    current = ""
    for i in range(lim_inf):
        current = alph[0]+current
    while(len(current)<=lim_sup):
        yield current
        current = wd.next_lex(current,alph)

def to_json(w1,w2,w3,l,m,b):
    data = {
        'w1': w1,
        'w2': w2,
        'w3': w3,
        'ways_to_shuffle':l,
        'ways_to_commute':m,
        'commuting_is_enough':b
    }
    json_str = json.dumps(data,indent=2)
    return json_str


gen1 = generate_increasing_words(alph,N,lim_inf=1)
gen2 = generate_increasing_words(alph,N,lim_inf=1)

with open("shuffles.txt",'w') as file:
    for w1 in gen1:
        for w2 in gen2:
            gen3 = generate_increasing_words(alph,len(w1)+len(w2),lim_inf=len(w1)+len(w2))
            for w3 in gen3:
                """ try:
                    L = sh.all_possible_shuffles(w1,w2,w3)
                    l = len(L)
                    S = L[0]
                    M = sh.all_possible_commutations(S)
                    m = len(M)
                    b = sh.compare_sets_of_shuffles(L,M)
                    s = to_json(w1,w2,w3,l,m,b)
                    file.write(s)
                    file.write("\n")
                except sh.ShuffleError:
                    continue  """
                print(
                    f"({w1},{w2},{w3})"
                )

