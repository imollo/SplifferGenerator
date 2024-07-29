def word_to_primitive(w):
    """
    Given a word w, it returns the unique
    primite word p such that w is in p*.
    """
    n = len(w)
    for i in range(1,n+1):
        if is_star_of(w,w[0:i]):
            return w[0:i]
        
def is_star_of(w,p):
    """
    Returns True if and only if w can be written as a 
    concatenation of copies of p.
    """
    n = len(w)    
    if n<len(p) or not n % len(p) == 0:
        return False
    
    p_2=p
    while(n>len(p_2)):
        p_2 = p_2+p
    return w == p_2

def quick_sort(w):
    """
    Executes the quick sort algorithm for lists.
    If used on a word, it returns an ordered list
    with its characters.
    """
    if len(w)==0:
        return w
    else:
        h = w[0]
        w_less = [c for c in w if c<h]
        w_mid = [c for c in w if c==h]
        w_great = [c for c in w if c>h]
        return quick_sort(w_less)+w_mid+quick_sort(w_great)

def is_permutation_of(u,v):
    u2 = quick_sort(u)
    v2 = quick_sort(v)
    return u2 == v2

def nub(w):
    """
    Given a word w, it returns the minimal
    alphabet A such that w is in A*.
    """
    s = quick_sort(w)
    try:
        alph =s[0]
    except IndexError:
        #print("La palabra es vacía")
        return ""  
    for c in s: 
        if c>alph[-1]:
            alph=alph+c
    return alph

def is_prefix(w1,w2):
    n = len(w1)
    m = len(w2)
    if (n>m):
        return False
    else:
        return w1==w2[0:n]

def is_greater_lex(w1,w2,alph):
    """
    Returns True iff <w1> is lexicographically greater than <w2>
    under the ordered alphabet <alph>.
    """
    if len(w1)>len(w2):
        return True
    elif len(w2)>len(w1):
        return False
    else:
        for i in range(len(w1)):
            if alph.find(w1[i])>alph.find(w2[i]):
                return True
            elif alph.find(w1[i])<alph.find(w2[i]):
                return False
            else:
                continue
        return False

def is_greater_or_equal_lex(w1,w2,alph):
    return is_greater_lex(w1,w2,alph) or w1==w2

def is_lesser_lex(w1,w2,alph):
    """
    Returns True iff <w1> is lexicographically lesser than <w2>
    under the ordered alphabet <alph>.
    """
    return is_greater_lex(w2,w1,alph)

def is_lesser_or_equal_lex(w1,w2,alph):
    return is_lesser_lex(w1,w2,alph) or w1==w2

def next_lex(w,alph):
    """
    Given a word and an ordered alphabet,
    returns the next word in lexicographic order.
    """
    l = alph[-1]
    new_w = ""
    for i in range(1,len(w)+1):
        j = alph.find(w[-i])
        new_char = alph[(j+1)%len(alph)]
        new_w = new_char+new_w
        if w[-i]!=l:
            new_w = w[-len(w):-i]+new_w
            break
        elif i==len(w):
            new_w = alph[0]+new_w
    if len(new_w)==0: #this is horrible but I'm in a hurry
        new_w = alph[0] 
    return new_w

def is_canonical_word(w,alph):
    """
    Takes a word and an ordered alphabet. It returns True iff
    w is its own canonical representative under ordered alphabet 
    isomorphisms. For instance, if alph='abcd' then the following
    are pairs of words such that the second is the canonical 
    representative of the first.

    * bda -----> abc
    * ccaaab ------> aabbbc
    * cdcdcdcdbbb -------> ababababccc
    """
    seen = ""
    for ch in w:
        if not ch in seen:
            seen = seen + ch
    return is_prefix(seen,alph)

def is_palindrome(w):
    return w==w[::-1]

def apply_permutation(c,alph,perm):
    """
    Takes a letter c on alph and a permutation on alph
    and applies the permutation to c.

    The permutation is represented as a permutation of 
    alph.
    """
    i = alph.find(c)
    return perm[i]

def conjugate(w,alph=None,perm=None):
    """
    perm is the permutation function on the alphabet.
    It's represented as a permutation of alph
    (considered as a word).
    """
    if alph==None:
        alph = nub(w)
    if perm==None:
        perm = alph[1:]+alph[0]
    w2 = ""
    for c in w:
        w2 = w2 + apply_permutation(c,alph,perm)
    return w2[::-1]

def is_self_adjoint(w,alph=None,perm=None):
    return w==conjugate(w,alph,perm)

def find_appropriate_permutation(w, alph=None):
    """
    Given a word w in alph, it returns the only permutation
    of alph (if it exists) such that w is equal to its 
    conjugate under that permutation.
    """
    if alph==None:
        alph = nub(w)
    plah = ""
    for c in alph:
        i = w.find(c)
        if i == -1:
            plah = plah+c
        else:
            anti_i = len(w)-i-1
            plah = plah+w[anti_i]
    if is_permutation_of(plah,alph):
        return plah
    else:
        return None

def enlengthen(c,n):
    """
    Takes a character c and repeats it
    n times to get a string. 
    """
    if n<0:
        raise ValueError()
    elif n==0:
        return ""
    else:
        return c+enlengthen(c,n-1)
    
def word_to_parikh(w, alph):
    p = []
    for c in alph:
        p.append(w.count(c))
    return p

def is_canonical_parikh(p):
    """
    Given a vector, it returns True iff 
    at least one canonical word has it
    as a Parikh vector. 
    """
    l = [i for i in range(len(p)) if p[i]==0]
    try:
        min = l[0]
    except IndexError:
        return True
    for j in range(len(l)):
        l[j] = l[j]-min
    return l==list(range(len(l)))

def parikh_to_min_word(p,alph):
    """
    It REQUIRES |alph|=|p|.
    It returns the minimal lexicographic 
    word w such that word_to_parikh(w)==p.
    """
    res = ""
    for i in range(len(alph)):
        res = res+enlengthen(alph[i],p[i])