import json
import sys

import shuffle as sh
import words as wd

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
    filename = "shuffles_to_"+str(N)+"_"+alph

    first_time = True
    with open(filename,'w') as file:
        file.write('[\n')
        gen1 = generate_increasing_words(alph,N,lim_inf=1)
        for w1 in gen1:
            gen2 = generate_increasing_words(alph,N,lim_inf=1)
            for w2 in gen2:
                gen3 = generate_increasing_words(alph,len(w1)+len(w2),lim_inf=len(w1)+len(w2))
                for w3 in gen3:
                    if not wd.is_canonical_word(w3,alph): #We don't want superfluous cases
                        continue
                    try:
                        L = sh.all_possible_shuffles(w1,w2,w3)
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
        
def add_shuffles_and_append(filename,alph,n,N):
    """
    Auxiliary function to complete shuffle files up to 
    an N>n input size.
    """
    new_filename = "shuffles_to_"+str(N)+"_"+alph

    with open(filename,'r') as file:
        json_data = json.load(file)
    gen1 = generate_increasing_words(alph,N)
    for w1 in gen1:
        gen2 = generate_increasing_words(alph,N,lim_inf=n)
        for w2 in gen2:
            gen3 = generate_increasing_words(alph,len(w1)+len(w2),lim_inf=len(w1)+len(w2))
            for w3 in gen3:
                if not wd.is_canonical_word(w3,alph):
                    continue
                try:
                    L = sh.all_possible_shuffles(w1,w2,w3)
                    l = len(L)
                    try:
                        S = L[0]
                        M = sh.all_possible_commutations(S)
                        m = len(M)
                        b = sh.compare_sets_of_shuffles(L,M)
                        d = to_dict(w1,w2,w3,l,m,b)
                        json_data.append(d)
                    except IndexError:
                        #print(f"{w1},{w2} cannot be shuffled into {w3}")
                        continue
                except sh.ShuffleError:
                    continue
    json_str = json.dumps(json_data,indent=2)
    with open(new_filename,'w') as file:
        file.write(json_str)

def main(alph,N):
    generate_shuffles_to_file(alph,N)

try:
    main(sys.argv[1],int(sys.argv[2]))
except:
    print(
        f"Usage: \npython3 {sys.argv[0]} <alph> <N>\n with:\n * <alph> a string of alphabet symbols \n * <N> the maximum length of the shuffling words to generate"
    )
    print(
        "A file called 'shuffles_to_<N>_<alph>' will be generated with the results."
    )