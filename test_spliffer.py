from spliffer import Spliffer

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

S.del_state("1")

S.display(horizontal=False)