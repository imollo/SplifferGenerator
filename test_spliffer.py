from spliffer import Spliffer
from diligent_spliffer import diligent_spliffer
from shuffle import Atom, Shuffle

alph="ab"
S = Spliffer(alph)

stt0 = S.add_state()
stt1 = S.add_state("1")
stt2 = S.add_state("dai")
S.set_initial(stt0)
S.set_final(stt2)

S.set_transition(stt0,"1","a","l")
S.set_transition("1",stt2,"b","r")
S.set_transition("dai","dai","a","r")

try:
    S.set_transition(stt1,stt1,"a","left")
except ValueError as error:
    print(error.args[0])

S.display()

print(
    f"The predecessors of state 2 are {S.predecessors(stt2)}."
    )
print(
    f"The predecessors of state 1 are {S.predecessors(stt1)}."
    )
print(
    f"The successors of state 1 are {S.successors(1)}"
)

al = Atom("a","l")
ar = Atom("a","r")
bl = Atom("b","l")
br = Atom("b","r")

M = Shuffle()
M.mix_in(al)
M.mix_in(br)
M.mix_in(ar)
M.mix_in(ar)

print(
    f"We wonder if the shuffle {[at.val for at in M.shuf()]} is accepted by S"
)
print(
    f"The answer is {S.accepts(M)}."
)

N = Shuffle()
N.mix_in(al)
N.mix_in(al)
N.mix_in(br)
N.mix_in(ar)
N.mix_in(ar)
print(
    f"now let's do the same with the shuffle f{[at.val for at in N.shuf()]}: is it accepted by S?"
)
print(
    f"the answer is {S.accepts(N)}"
)