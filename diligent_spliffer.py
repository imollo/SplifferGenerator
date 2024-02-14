from spliffer import Spliffer
from words import word_to_primitive, nub

def diligent_spliffer(l,r,s,alph=""):
    l = word_to_primitive(l)
    r = word_to_primitive(r)
    s = word_to_primitive(s)
    
    if alph == "":
        alph = nub(l+r+s)

    D = Spliffer(alph)
    D.add_state(name="0,0,0")
    D.set_initial("0,0,0")
    D.set_final("0,0,0")

    visited = []

    while(len(visited)<len(D.states())):
        L = [ v for v in D.states().values() if v not in visited ]
        n = L[0]
        t = name_to_tuple(n)
        if l[t[0]] == s[t[2]]:
            t_new_left = add_one_to_tuple(l,r,s,t,pos='l')
            n_new_left = tuple_to_name(t_new_left)
            if not n_new_left in D.states().values():
                D.add_state(n_new_left)
            D.set_transition(n,n_new_left,s[t[2]],pos='l')
        if r[t[1]] == s[t[2]]:
            t_new_right = add_one_to_tuple(l,r,s,t,pos='r')
            n_new_right = tuple_to_name(t_new_right)
            if not n_new_right in D.states().values():
                D.add_state(n_new_right)
            D.set_transition(n,n_new_right,s[t[2]],pos='r')
        visited.append(n)

    return D

def name_to_tuple(n):
    """
    Takes string of the form 'i,j,k' where i,j,k are numbers
    and transforms it into list [i,j,k]
    """
    return list(map(int,n.split(',')))

def tuple_to_name(t):
    """
    Takes list of the form '[i,j,k]' where i,j,k are numbers
    and transforms it into string 'i,j,k'
    """
    n = str(t[0])
    n = n+','+str(t[1])
    n = n+','+str(t[2])
    return n

def add_one_to_tuple(l,r,s,t,pos):
    """
    Takes list of numbers of the form '[i,j,k]' and adds one
    in positions: 
    * 0 and 2 when pos='l'
    * 1 and 2 when pos='r'
    The sum is performed modulo |l|,|r|,|s| in positions
    0, 1, 2 respectively
    """
    t_new = t.copy()
    if pos in ['l','L']:
        t_new[0] += 1
        t_new[0] %= len(l)
    elif pos in ['r','R']:
        t_new[1] += 1
        t_new[1] %= len(r)
    elif not isinstance(pos,str):
        raise TypeError(
            "pos should be either 'l' or 'r'"
        )
        return
    else:
        raise ValueError(
            "pos should be either 'l' or 'r'"
        )
    t_new[2] += 1
    t_new[2] %= len(s)
    return t_new
         