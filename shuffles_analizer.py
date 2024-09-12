import json
import ijson #Iterative json parser

import os

import graphviz

import words as wd
import shuffle as sh
import diligent_spliffer as dil

def retrieve_json_data(filename):
    """
    To parse the json data, we use ijson
    instead of json, so that we are not 
    loading a big (>3GB) json file in memory.
    """
    with open(filename, 'r') as f:
        parser = ijson.items(f, 'item')
        for item in parser:
            yield item

def test_give_last_thing(filename):
    with open(filename, 'r') as f:
        parser = ijson.items(f, 'item')
        last_item = None
        try:
            for item in parser:
                last_item = item
        except ijson.common.IncompleteJSONError:
            print(last_item)
    print(last_item)

def find_alph_from_filename(filename):
    """
    Esto es horrible, lo hago para encontrar el alfabeto a partir del filename
    El alfabeto suele venir después del número en el formato de nombres que estoy usando
    e.g. "shuffle_to_5_ab_counterexamples" o "shuffle_to_3_abcd"
    """
    alph=""
    l = filename.split("_")
    for i in range(len(l)):
        if l[i].isdigit():
            alph = l[i+1]
            break
    return alph

def build_diligent_spliffers(filename):
    folder_name = filename+"_diligent_spliffers"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    alph = find_alph_from_filename(filename)

    for thing in retrieve_json_data(filename):
        try:
            w1 = thing["w1"]
            w2 = thing["w2"]
            w3 = thing["w3"]
            S = dil.diligent_spliffer(w1,w2,w3,alph)
            new_file = folder_name+"/"+w1+"_"+w2+"_"+w3
            S._A.save(new_file,format="dot") #esto no se hace pero no reimplementé awalipy.save en Spliffer
            S._A.save(new_file+".json",format="json")
            graphviz.render('dot','png',new_file)
            os.remove(new_file)
        except (IndexError,TypeError):
            continue

def to_json_generators(w1,w2,w3,L):
    d = {"w1":w1,"w2":w2,"w3":w3,"p":str(L)}
    json_str = json.dumps(d,indent=2)
    return json_str

def classify_by_primitive_generators(filename):
    """
    Takes the filename of a shuffle file, and classifies its contents
    by the primitive words that make up the shuffles.

    It records which (n,m,k) are possible powers for each tuple of
    primitive words (l,r,s), and lists them all in output file.    
    """

    left_primitives = {}

    new_filename = filename+"_by_generators"

    print(f"Reading data from {filename}...",end="")
    json_data = retrieve_json_data(filename)
    print("Done.")

    for thing in json_data:
        try:
            w1 = thing["w1"]
            w2 = thing["w2"]
            w3 = thing["w3"]
            P = sh.reduce_to_primitive_representation(w1,w2,w3)
            lp,rp,sp = P[0][0],P[1][0],P[2][0]
            ln,rn,sn = P[0][1],P[1][1],P[2][1]
            if not lp in left_primitives.keys():
                left_primitives[lp] = {}
            if not rp in left_primitives[lp].keys():
                left_primitives[lp][rp] = {}
            if not sp in left_primitives[lp][rp].keys():
                left_primitives[lp][rp][sp] = []
            left_primitives[lp][rp][sp].append((ln,rn,sn))
        except:
            pass

    first_time = True
    with open(new_filename,"w") as file:
        file.write('[')
        for k1 in left_primitives.keys():
            for k2 in left_primitives[k1].keys():
                for k3 in left_primitives[k1][k2].keys():
                    json_str = to_json_generators(k1,k2,k3,left_primitives[k1][k2][k3])
                    if first_time:
                        file.write("\n")
                        first_time = False
                    else:
                        file.write(",\n")
                    file.write(json_str)
        file.write('\n]')
    

def filter_by(filename,new_filename,function):
    """
    Takes the <filename> of an existing json file, a <new_filename> and
    a boolean <function>. It filters <filename> by the value of <function>
    and dumps the filtered file onto <new_filename>.
    Now lazy! 
    """
    filtered = []

    print("Starting the filtering process...",end="")
    total = 0
    for thing in retrieve_json_data(filename):
        try:
            if function(thing):
                filtered.append(thing)
            total = total+1
        except BaseException:
            continue
    print("Done.")
    
    filtered.insert(0,str(len(filtered))+" elements filtered out of "+str(total)+".")
    json_str = json.dumps(filtered,indent=2)

    print(f"Writing filtered data to {new_filename}...", end="")
    with open(new_filename,'w') as file:
        file.write(json_str)
    print("Done.")
    print("Filtering process complete.")

def filter_counterexamples(filename):
    """
    Filters <filename> for all tuples (w1,w2,w3) that have
    been marked with False regarding the commutativity being
    enough to generate all possible ways to shuffle them.

    It dumps the results in '<filename>_counterexamples'.
    """
    filename_counter = filename+"_counterexamples"
    def check_commutativity_not_enough(thing):
        return not thing["commuting_is_enough"]
    filter_by(filename,filename_counter,check_commutativity_not_enough)
    

def filter_essential_counterexamples(filename):
    """
    Filters <filename> for all tuples (w1,w2,w3) that do NOT have redundant
    commutativity at the beginning or end of their shuffles.
    """
    new_filename = filename+"_essential"
    def check_for_redundant_commutativity(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        w3 = thing["w3"]
        res = sh.have_initial_or_final_redundant_commutativity(w1,w2,w3)
        return not res
    filter_by(filename,new_filename,check_for_redundant_commutativity)

def filter_by_palindromy(filename):
    new_filename = filename+"_palindromic"
    def check_palindromic(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        w3 = thing["w3"]
        res = wd.is_palindrome(w1) and wd.is_palindrome(w2) and wd.is_palindrome(w3)
        return res
    filter_by(filename,new_filename,check_palindromic)

def filter_by_unpalindromy(filename):
    new_filename = filename+"_not_palindromic"
    def check_unpalindromicy(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        w3 = thing["w3"]
        res = not (wd.is_palindrome(w1) and wd.is_palindrome(w2) and wd.is_palindrome(w3))
        return res
    filter_by(filename,new_filename,check_unpalindromicy)

def filter_by_conjugacy(filename):
    """"
    Requires binary alphabet.
    """
    new_filename = filename+"_conjugacy"
    def check_conjugacy(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        w3 = thing["w3"]
        alph = find_alph_from_filename(filename)
        plah = wd.find_appropriate_permutation(w3,alph=alph)
        if plah==None:
            return False
        else:
            res = wd.is_self_adjoint(w1,alph=alph,perm=plah) and wd.is_self_adjoint(w2,alph=alph,perm=plah) and wd.is_self_adjoint(w3,alph=alph,perm=plah)
            return res
    filter_by(filename,new_filename,check_conjugacy)

def filter_by_unconjugacy(filename):
    new_filename = filename+"_not_conjugacy"
    def check_non_conjugacy(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        w3 = thing["w3"]
        alph = find_alph_from_filename(filename)
        plah = wd.find_appropriate_permutation(w3,alph=alph)
        if plah==None:
            return True
        else:
            res = wd.is_self_adjoint(w1,alph=alph,perm=plah) and wd.is_self_adjoint(w2,alph=alph,perm=plah) and wd.is_self_adjoint(w3,alph=alph,perm=plah)
            return not res
    filter_by(filename,new_filename,check_non_conjugacy)

def filter_by_input_equality(filename):
    new_filename = filename+"_equals"
    def check_equality(thing):
        return thing["w1"]==thing["w2"]
    filter_by(filename,new_filename,check_equality)

def filter_by_input_inequality(filename):
    new_filename = filename+"_not_equals"
    def check_inequality(thing):
        return thing["w1"]!=thing["w2"]
    filter_by(filename,new_filename,check_inequality)

def filter_by_includedness(filename):
    new_filename = filename+"_not_input_included"
    def check_not_included(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        return (not (w1 in w2)) and (not (w2 in w1))
    filter_by(filename,new_filename,check_not_included)

def filter_by_prefix(filename):
    new_filename = filename+"_prefix"
    def check_if_prefix(thing):
        w1 = thing["w1"]
        w2 = thing["w2"]
        return (wd.is_prefix(w1,w2))
    filter_by(filename,new_filename,check_if_prefix)
    
def filter_by_commutative_classes(filename):
    """
    A filter which looks at the number of commutative classes
    in each thing["ways_to_commute"] and keeps only the ones
    with three classes or more.
    """
    new_filename = filename+"_too_many_classes"
    def check_number_of_classes(thing):
        n_classes = len(thing["ways_to_commute"])
        return n_classes>2
    filter_by(filename,new_filename,check_number_of_classes)

def main(option, filename):
    if option == "counterexamples":
        filter_counterexamples(filename)
    elif option == "diligent":
        build_diligent_spliffers(filename)
    elif option == "essential":
        filter_essential_counterexamples(filename)
    elif option == "palindrome":
        filter_by_palindromy(filename)
    elif option == "not_palindrome":
        filter_by_unpalindromy(filename)
    elif option == "conjugate":
        filter_by_conjugacy(filename)
    elif option == "not_conjugate":
        filter_by_unconjugacy(filename)
    elif option == "included":
        filter_by_includedness(filename)
    elif option == "equality":
        filter_by_input_equality(filename)
    elif option == "inequality":
        filter_by_input_inequality(filename)
    elif option == "primitives":
        classify_by_primitive_generators(filename)
    elif option == "prefix":
        filter_by_prefix(filename)
    elif option == "too_many_classes":
        filter_by_commutative_classes(filename)
    else:
        raise ValueError