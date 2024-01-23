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
        self.pos = pos
        self.val = [ch,"",ch] if pos in ['l','L'] else ["",ch,ch]

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

    def mix_in(self,at):
        self._s.append(at)
        if at.pos in ['l','L']:
            self._v[0]+=at.ch
        elif at.pos in ['r','R']:
            self._v[1]+=at.ch
        self._v[2]+=at.ch

    def pop(self):
        a = self._s.pop()
        self._v[2] = self._v[2][:-1]
        if a.pos in ['l','L']:
            self._v[0] = self._v[0][:-1]
        elif a.pos in ['r','R']:
            self._v[1] = self._v[1][:-1]

    def shuf(self):
        return self._s

    def val(self):
        return self._v
    
    # I think this works but I didn't need it    
"""     def pop_first(self):
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

def all_possible_shuffles(l,r,s):
    """
    Given three words l,r,s it returns a list of all
    possible Shuffles such that their values are (l,r,s)
    """
    pass