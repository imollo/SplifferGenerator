import awalipy

class Spliffer:
    def __init__(self, alph):
       self._A = awalipy.Transducer([alph,alph,alph])
       self._states = {} 

    def add_state(self,name=""):
        """ 
        Usage: Spliffer.add_state(self, name="")
        assigns name to state and returns (awalipy.stt,name)
        when it is not empty, returns only awalipy.stt otherwise. 
        """
        stt = self._A.add_state(name)
        self._states[stt] = name
        return stt if name=="" else (stt,name)
    
    def del_state(self,stt):
        """
        Usage: Spliffer.del_state(self,stt)
        stt can be either a tuple (awalipy.stt, name)
          or merely awalipy.stt
        """
        if isinstance(stt,tuple):
            stt_0 = stt_0[0]
        elif isinstance(stt,str):
            stt = self._find_stt_from_name(stt)
        self._states.pop(stt)
        self._A.del_state(stt)
         # awalipy.del_state gets rid of all transitions for us
    
    def states(self):
        return self._states
    
    def set_initial(self,stt):
        if isinstance(stt,tuple):
            stt = stt[0]
        elif isinstance(stt,str):
            stt = self._find_stt_from_name(stt)

        self._A.set_initial(stt)

    def set_final(self,stt):
        if isinstance(stt,tuple):
            stt = stt[0]
        elif isinstance(stt,str):
            stt = self._find_stt_from_name(stt)
            
        self._A.set_final(stt)
    
    def set_transition(self, stt_0,stt_1,ch,pos):
        """
        Usage: Spliffer.set.transition(self,stt_0,stt_1,ch,pos)
        stt_0, stt_1 can be either a tuple (awalipy.stt,name), 
          merely awalipy.stt
          or the given name of the state
        ch is the character of the transition
        pos can be either 'l', 'L', 'r', 'R'         
        """
        if isinstance(stt_0,tuple):
            stt_0 = stt_0[0]
        elif isinstance(stt_0,str):
            stt_0 = self._find_stt_from_name(stt_0)

        if isinstance(stt_1,tuple):
            stt_1 = stt_1[0]
        elif isinstance(stt_1,str):
            stt_1 = self._find_stt_from_name(stt_1)

        if pos in ['l','L']:
            self._A.set_transition(stt_0,stt_1,[ch,"",ch])
        elif pos in ['r','R']:
            self._A.set_transition(stt_0,stt_1,["",ch,ch])
        elif not isinstance(pos, str):
            raise TypeError(
                f"last argument should be 'l' or 'r'"
            )
        else:
            raise ValueError(
                f"last argument should be 'l' or 'r'"
            )
    
    def del_transition(self,tr):
        self.A.del_transition(tr)

    def _find_stt_from_name(self,name):
        stt = -1
        for key in self._states.keys():
            if self._states[key]==name:
                stt=key
                break
        if stt >= 0:
            return stt
        else:
            raise ValueError(
                f"name does not match any state of Spliffer"
            )

    def display(self, horizontal=True):
        self._A.display(horizontal)