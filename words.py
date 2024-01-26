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
        print("La palabra es vacía")
        return ""  
    for c in s: 
        if c>alph[-1]:
            alph=alph+c
    return alph

#def is_prefix(w1,w2):
    #n = len(w1)
    #m = len(w2)
    #if (n>m):
        #return False
    #else:
        #return w1==w2[0:n]
