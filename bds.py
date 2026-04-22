from spliffer import Spliffer
from words import nub

def left_bds(w,alph=""):
    n = len(w)

    if alph == "":
        alph = nub(w)

    D = Spliffer(alph)
    D.add_state(name="0,0")
    D.set_initial("0,0")
    D.set_final("0,0")

    for k in range(0,n): # we are taking k the minimum and it has to be lesser than n
        for l in range(k,k+n+1):
            new_state_name=str(k)+","+str(l)
            D.add_state(name=new_state_name)
    
    for p in D.states():
        p_name = D._A.get_state_name(p)
        [k,l] = p_name.split(",")
        k_int = int(k)
        l_int = int(l)
        if k_int == 0:
            if l_int-k_int < n:
                target_state_name = str(n-1)+","+str(n+l_int)
                D.set_transition(p_name,target_state_name,w[0],"l")
            if l_int > 0:
                right_target_state_name = k+","+str(l_int-1)
                new_right_char = w[(n-l_int)%n]
                D.set_transition(p_name,right_target_state_name,new_right_char,"r")
        elif k_int != 0:
            if l_int-k_int == 0:
                target_state_name = str(k_int-1)+","+l
                new_char = w[(n-k_int)%n]
                D.set_transition(p_name,target_state_name,new_char,"l")
            if l_int-k_int < n:
                left_target_state_name = str(k_int-1)+","+l
                new_left_char = w[(n-k_int)%n]
                D.set_transition(p_name,left_target_state_name,new_left_char,"l")
            if l_int-k_int > 0: 
                right_target_state_name = k+","+str(l_int-1)
                new_right_char = w[(n-l_int)%n]
                D.set_transition(p_name,right_target_state_name,new_right_char,"r")

    D.trim()
    
    return D