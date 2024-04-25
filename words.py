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

def is_lesser_lex(w1,w2,alph):
    """
    Returns True iff <w1> is lexicographically lesser than <w2>
    under the ordered alphabet <alph>.
    """
    return is_greater_lex(w2,w1,alph)

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

def conjugate(w,alph=None):
    """
    Requires binary alphabet.
    """
    if alph==None:
        alph_1=nub(w)
        if len(alph_1)!=2:
            raise ValueError(
                "Need a two-symbol alphabet."
            )
        else:
            alph = alph_1

    w2 = ""
    for i in range(len(w)):
        if w[i] == alph[0]:
            w2 = w2+alph[1]
        else:
            w2 = w2+alph[0]
    return w2

def is_self_adjoint(w,alph=None):
    """
    Requires binary alphabet.
    """
    return w==conjugate(w,alph)[::-1]
