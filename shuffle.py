from termcolor import colored #for Shuffle.__repr__

import words #necessary for words.nub

class Atom:
    def __init__(self,ch,pos):
        if not isinstance(pos,str):
            raise TypeError(
                "pos should be 'l' or 'r'"
            )
        elif not pos in ['l','r','L','R']:
            raise ValueError(
                "pos should be 'l' or 'r'"
            )
        self.ch  = ch
        self.pos = 'l' if pos in ['l','L'] else 'r'
        self.val = [ch,"",ch] if pos in ['l','L'] else ["",ch,ch]

    def __str__(self):
        return str(self.val)
    
    def __repr__(self):
        return f"Atom: ({self.ch},{self.pos})"

    def __eq__(self,other):
        return self.ch==other.ch and self.pos==other.pos

    @staticmethod
    def concatenate(L):
        """
        Takes a list of atoms and concatenates them,
        returning a list of three strings.
        """
        res = ["","",""]
        for at in L:
            res[0] += at.val[0]
            res[1] += at.val[1]
            res[2] += at.val[2]
        return res
    
    @staticmethod
    def alph_to_atoms(alph):
        """
        Takes an alphabet string and returns a dictionary
        containing all possible atoms for that alphabet.

        For each character ch in the alphabet and each position
        pos in {'l','r'}, the key for obtaining Atom(ch,pos) from
        the dictionary is <ch_pos>. For instance,
        alph_to_atoms("abcd")["b_l"] returns Atom('b','l').   
        """
        alph = words.nub(alph) #removes duplicates
        d = {}
        for ch in alph:
            key_l = ch+"_l"
            key_r = ch+"_r"
            d[key_l] = Atom(ch,'l')
            d[key_r] = Atom(ch,'r')
        return d


class Shuffle:
    def __init__(self):
        self._s = []
        self._v = ["","",""]

    def __len__(self):
        return len(self._s)
    
    def __getitem__(self,key):
        S = Shuffle()
        if isinstance(key,int):
            S._s = [self._s[key]]
        elif isinstance(key,slice):
            S._s = self._s[key]
        else:
            raise ValueError(
                "invalid subscripted value for Shuffle object"
            )
        S._v = Atom.concatenate(S._s)
        return S
    
    def __repr__(self):
        str = ""
        for at in self._s:
            if at.pos=='l':
                aux_str = colored(at.ch,"white","on_red")
            elif at.pos=='r':
                aux_str = colored(at.ch,"white","on_blue")
            str = str+aux_str
        return str
        #return self._s.__repr__()

    def __str__(self):
        return self.__repr__()

    def __eq__(self,other):
        return self._s==other._s and self._v==other._v

    """
    # This doesn't appear to be working? 
    def __copy__(self):
        copy_instance = Shuffle()
        copy_instance._s = self._s
        copy_instance._v = self._v
        return copy_instance 
    """

    def display(self):
        print(self.__repr__())

    def mix_in(self,at):
        """
        Adds Atom at the end.
        """
        self._s.append(at)
        if at.pos in ['l','L']:
            self._v[0]+=at.ch
        elif at.pos in ['r','R']:
            self._v[1]+=at.ch
        self._v[2]+=at.ch

    def mix_beneath(self,at):
        """
        Adds Atom at the beginning.
        """
        self._s.insert(0,at)
        if at.pos in ['l','L']:
            self._v[0]=at.ch+self._v[0]
        elif at.pos in ['r','R']:
            self._v[1]=at.ch+self._v[1]
        self._v[2]=at.ch+self._v[2]

    def pop(self):
        a = self._s.pop()
        self._v[2] = self._v[2][:-1]
        if a.pos in ['l','L']:
            self._v[0] = self._v[0][:-1]
        elif a.pos in ['r','R']:
            self._v[1] = self._v[1][:-1]
        return a

    def shuf(self):
        return self._s

    def val(self):
        return self._v
    
    def simply_commutes_with(self,other):
        """
        Returns True if self and other have values
        (w,"",w) and ("",w,w)
        for some word w. 
        """
        b0 = self._v[0]==other._v[1]
        b1 = self._v[1]==other._v[0]
        b2 = self._v[2]==other._v[2]
        b3 = (self._v[0]=="" or self._v[1]=="")
        return (b0 and b1 and b2 and b3)

"""  # I think this works but I didn't need it    
     def pop_first(self):
        if len(self._s)==0:
            raise IndexError(
                "shuffle is empty"
            )
        p = self._s[0].pos
        del(self._s[0])
        if p in ['l','L']:
            self._v[0] = self._v[0][1:]
        elif p in ['r','R']:
            self._v[1] = self._v[1][1:]
        self._v[2] = self._v[2][1:]
 """

class ShuffleError(BaseException):
    pass

def all_possible_shuffles(l,r,s):
    """
    Given three words l,r,s it returns a list of all
    possible Shuffles such that their values are (l,r,s)
    """
    if not len(l)+len(r)==len(s):
        raise ShuffleError(
            f"the length of the arguments is wrong for a valid shuffle"
        )
    
    alph = words.nub(l+r+s)
    for ch in alph:
        if not l.count(ch)+r.count(ch)==s.count(ch):
            raise ShuffleError(
                f"wrong count of character {ch} in arguments for a valid shuffle"
            )

    if len(s)==0:
        S = Shuffle()
        return [S]
    else:
        res = []
        if len(l)>0 and l[0] == s[0]:
            L = all_possible_shuffles(l[1:],r,s[1:])
            for S in L:
                S.mix_beneath(Atom(l[0],'l'))
                res.append(S)

        if len(r)>0 and r[0] == s[0]:
            L = all_possible_shuffles(l,r[1:],s[1:])
            for S in L:
                S.mix_beneath(Atom(r[0],'r'))
                res.append(S)

        return res

def can_be_shuffled(l,r,s):
    """
    Returns True iff the words l,r can be shuffled
    to obtain the word s.
    """
    L = all_possible_shuffles(l,r,s)
    return len(L)>0

def all_simple_commutations(S):
    """
    Takes a Shuffle S and returns a list of all possible Shuffles
    arising from a single simple commutation of sub-shuffles of S.
    """
    res = [S]
    
    if len(S) == 0:
        return res
    #We may assume S is non-empty

    switches = [0]
    switches.extend([i for i in range(1,len(S)) 
                     if S.shuf()[i].pos != S.shuf()[i-1].pos])
    sub_shufs = [S[switches[i-1]:switches[i]] for i in range(1,len(switches))]
    sub_shufs.append(S[switches[-1]:])
    
    for i in range(1,len(sub_shufs)):
        sub = sub_shufs[i]
        sub_p = sub_shufs[i-1]
        n = min(len(sub),len(sub_p))
        
        for k in range(1,n+1):
            if sub[:k].val()[2]==sub_p[-k:].val()[2]:
                #This should be replaced with T = S.copy() when I learn how to do it
                T = Shuffle()
                T._s = S.shuf().copy()
                T._v = Atom.concatenate(T._s)
                ####
                T.shuf()[switches[i]-k:switches[i]]=sub[:k].shuf()
                T.shuf()[switches[i]:switches[i]+k]=sub_p[-k:].shuf()
                # we don't need to change the value as this operation preserves it
                res.append(T)

    return res

#This function can probably be optimized but right now it doesn't seem worth the trouble
def are_a_simple_comm_away(S1,S2):
    return S2 in all_simple_commutations(S1)

def all_possible_commutations(S):
    to_visit = [S]
    visited = []
    while len(to_visit)>0:
        T = to_visit.pop()
        if T not in visited:
            visited.append(T)
            L = all_simple_commutations(T)
            to_visit.extend(L)
    return visited

def compare_sets_of_shuffles(l1,l2):
    """
    Given two lists of Shuffles, returns True if they are 
    equal as sets (i.e. their elements are the same, could be
    in different order)
    """
    for s in l1:
        if not s in l2:
            return False
    for s in l2:
        if not s in l1:
            return False
    return True

def have_initial_or_final_redundant_commutativity(l,r,s):
    """
    Takes three words (l,r,s) and returns True iff
    there's an initial or final Atom which appears always to
    commutative distance of any Shuffle.
    """
    alph = words.nub(l+r+s)
    L = all_possible_shuffles(l,r,s)
    S0 = L[0]
    try:
        at_l_i = Atom(l[0],'l')
        at_l_f = Atom(l[-1],'l')
        at_r_i = Atom(r[0],'r')
        at_r_f = Atom(r[-1],'r')
    except IndexError as err:
        print(err)
    suspected_atoms = {"l_i":True,"r_i":True,"l_f":True,"r_f":True}
    visited_shuffles = []
    for s in L:
        if s in visited_shuffles:
            continue
        M = all_possible_commutations(s)
        visited_shuffles.extend(M)
        appears = {"l_i":False,"r_i":False,"l_f":False,"r_f":False}
        for c in M:
            if at_l_i == c.shuf()[0]:
                appears["l_i"] = True
            if at_l_f == c.shuf()[-1]:
                appears["l_f"] = True
            if at_r_i == c.shuf()[0]:
                appears["r_i"] = True
            if at_r_f == c.shuf()[-1]:
                appears["r_f"] = True
        for k in appears.keys():
            if not appears[k]:
                suspected_atoms[k] = False
    res = False
    for k in suspected_atoms.keys():
        res = res or suspected_atoms[k]
    return res

    