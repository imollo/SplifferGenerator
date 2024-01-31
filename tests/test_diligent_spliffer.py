from diligent_spliffer import diligent_spliffer, name_to_tuple, tuple_to_name, add_one_to_tuple

l = "aabb"
r = "ba"
s = "ab"

T=[0,0,0]
N = tuple_to_name(T)
print("la tupla inicial es ", T, " y su nombre es ", N)

T_new = add_one_to_tuple(l,r,s,T,'l')
N_new = tuple_to_name(T_new)
N_ref = name_to_tuple(N_new)

print("la tupla luego de añadir uno en el lado izquierdo es ", T_new, " y su nombre es ", N_new)

T_new_new = add_one_to_tuple(l,r,s,T_new,'l')
N_new_new = tuple_to_name(T_new_new)
N_new_new_ref = name_to_tuple(N_new_new)

print("Lo hago otra vez y obtengo la tupla ", T_new_new, "con nombre ", N_new_new)

T_right = add_one_to_tuple(l,r,s,T_new_new,'r')
N_right = tuple_to_name(T_right)
N_right_ref = name_to_tuple(N_right)

print(T_right,N_right)

print("Si transformo los nombres que obtuve a tuplas me queda:")
print(N_ref,N_new_new_ref,N_right_ref)

D = diligent_spliffer(l,r,s)

D.display()

L_l = ["aabb", "aabb", "ababab", "aabbaabb"]
L_r = ["ba", "bababababa", "baba", "bababa"]
L_s = ["ab","ababababababab", "ababababab", "ababababababab"]
L_b = [True,True,False,True]