from shuffle import Atom, Shuffle, ShuffleError, all_possible_shuffles, all_simple_commutations, are_a_simple_comm_away, all_possible_commutations,compare_sets_of_shuffles

al = Atom("a","l")
ar = Atom("a","r")
bl = Atom("b","l")
br = Atom("b","r")
cl = Atom("c",'l')

print(f"al has value {al.val}")
print(f"br has value {br.val}")

S = Shuffle()
S.mix_in(al)
S.mix_in(bl)
S.mix_in(al)
S.mix_in(br)
S.mix_in(ar)
S.mix_in(bl)
print(
    f"the Shuffle S consists of {[at.val for at in S.shuf()]} with overall value {S.val()}"
)

S1 = S[2:5]
print(
    f"the sliced Shuffle S1 consists of {[at.val for at in S1.shuf()]} with overall value {S1.val()}"
)

S.pop()

print(
    f"after popping, the Shuffle S consists of {[at.val for at in S.shuf()]} with overall value {S.val()}"
)

S.mix_beneath(cl)
print(
    f"after mixing beneath a c, the Shuffle S consists of {[at.val for at in S.shuf()]} with overall value {S.val()}"
)

l = ["abb","","aabb", "aabbaabb","a",""]
r = ["caca","b","baba", "bababa","",""]
s = ["z","b","abababab", "ababababababab","a",""]

shufs = []
for i in range(len(s)):
    try:
        t = all_possible_shuffles(l[i],r[i],s[i])
        shufs.append(t)
    except BaseException as inst:
        shufs.append([inst])
        continue

for i in range(len(s)):
    print(
        f"las palabras {(l[i],r[i])} se pueden mezclar de {len(shufs[i])} maneras para formar la palabra '{s[i]}'"
    )
    print(
        f"los shuffles correspondientes son los siguientes:"
    )
    for t in shufs[i]:
        try:
            print([at.val for at in t.shuf()])
        except AttributeError:
            print(t)

T = Shuffle()
T.mix_in(ar)
T.mix_in(br)
T.mix_in(al)
T.mix_in(bl)
T.mix_in(ar)
T.mix_in(bl)
T.mix_in(al)

T2 = Shuffle()
T2.mix_in(ar)
T2.mix_in(br)
T2.mix_in(ar)
T2.mix_in(al)
T2.mix_in(bl)
T2.mix_in(al)

print(
    f"el valor de T es {T.val()} y los átomos están mezclados así:"
)
print(T)
print(
    f"el valor de T2 es {T2.val()} y los átomos están mezclados así:"
)
print(T2)

L = all_simple_commutations(T)
print(
    f"hay {len(L)} conmutaciones simples posibles que se pueden obtener a partir de T:"
)
for s in L:
    print(s)

L = all_simple_commutations(T2)
print(
    f"hay {len(L)} conmutaciones simples posibles que se pueden obtener a partir de T2:"
)
for s in L:
    print(s)

print(
    f"y T2 está a una conmutación simple de T: {are_a_simple_comm_away(T,T2)}"
    )

print(
    f"Estas son todas las posibles conmutaciones asociadas a T:"
)
L2 = all_possible_commutations(T)
for s in L2:
    print(s)

print(
    f"en el caso de T, ¿es cierto que todos los shuffles obtenidos por conmutaciones son todos los shuffles en general?"
)
u,v,w = T.val()
M = all_possible_shuffles(u,v,w)
print(compare_sets_of_shuffles(L2,M))

for s in M:
    print(s)