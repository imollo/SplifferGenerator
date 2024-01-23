from shuffle import Atom, Shuffle

al = Atom("a","l")
ar = Atom("a","r")
bl = Atom("b","l")
br = Atom("b","r")


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