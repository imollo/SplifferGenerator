from shuffle import Atom, Shuffle, ShuffleError, all_possible_shuffles, all_simple_commutations

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
T.mix_in(al)
T.mix_in(bl)
T.mix_in(al)
T.mix_in(ar)
T.mix_in(br)
T.mix_in(ar)
print(
    f"el valor de T es {T.val()} y los átomos están mezclados así:"
)
print(T)
T2 = all_simple_commutations(T)
print(
    f"hay {len(T2)} conmutaciones posibles que se pueden obtener a partir de T:"
)
for s in T2:
    print(s)
