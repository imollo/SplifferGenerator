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
        stt = self._find_stt_id_from_stt(stt)
        self._states.pop(stt)
        self._A.del_state(stt)
         # awalipy.del_state gets rid of all transitions for us
    
    def states(self):
        return self._states
    
    def set_initial(self,stt):
        stt = self._find_stt_id_from_stt(stt)
        self._A.set_initial(stt)

    def initial_states(self,with_names=False):
        if with_names:
            to_treat = self._A.initial_states()
            return [(stt,self._states[stt]) if not self._states[stt]=="" else stt 
                for stt in to_treat]
        else:
            return self._A.initial_states()
    
    def is_initial(self,stt):
        stt = self._find_stt_id_from_stt(stt)
        return stt in self._A.initial_states()

    def accesible_states(self, with_names=False):
        visited = self.initial_states()
        while True:
            new_visited = visited.copy()
            for stt in visited:
                l = self.successors(stt)
                succ = [sttt for sttt in l if not sttt in new_visited]
                new_visited.extend(succ)
            if len(visited)==len(new_visited):
                break
            else:
                visited = new_visited.copy()
        if with_names:
            return [(stt,self._states[stt]) if self._states[stt]!="" else stt
                    for stt in visited]
        else:
            return visited

    def set_final(self,stt):
        stt = self._find_stt_id_from_stt(stt)
        self._A.set_final(stt)
    
    def final_states(self, with_names=False):
        if with_names:
            to_treat = self._A.final_states()
            return [(stt,self._states[stt]) if not self._states[stt]=="" else stt 
                    for stt in to_treat]
        else:
            return self._A.final_states()
    
    def is_final(self,stt):
        stt = self._find_stt_id_from_stt(stt)
        return stt in self._A.final_states()

    def coaccesible_states(self, with_names=False):
        visited = self.final_states()
        while True:
            new_visited = visited.copy()
            for stt in visited:
                l = self.predecessors(stt)
                pred = [sttt for sttt in l if not sttt in new_visited]
                new_visited.extend(pred)
            if len(visited)==len(new_visited):
                break
            else:
                visited = new_visited.copy()
        if with_names:
            return [(stt,self._states[stt]) if self._states[stt]!="" else stt
                    for stt in visited]
        else:
            return visited

    def useful_states(self,with_names=False):
        L = [stt for stt in self.accesible_states(with_names=with_names) 
             if stt in self.coaccesible_states(with_names=with_names)]
        return L
    
    def trim(self):
        """
        Removes useless states from a Spliffer.
        """
        useful = self.useful_states()
        states = list(self._states.keys()).copy()
        for stt in states:
            if not stt in useful:
                self.del_state(stt)
        
    def set_transition(self, stt_0,stt_1,ch,pos):
        """
        Usage: Spliffer.set.transition(self,stt_0,stt_1,ch,pos)
        stt_0, stt_1 can be either a tuple (awalipy.stt,name), 
          merely awalipy.stt
          or the given name of the state
        ch is the character of the transition
        pos can be either 'l', 'L', 'r', 'R'         
        """
        stt_0 = self._find_stt_id_from_stt(stt_0)
        stt_1 = self._find_stt_id_from_stt(stt_1)

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

    def predecessors(self,stt,label=None,with_names=False):
        stt = self._find_stt_id_from_stt(stt)
        if with_names:
            return [(sttt,self._states[sttt]) if not self._states[sttt]=="" else sttt 
                     for sttt in self._A.predecessors(stt,label)]
        else:
            return self._A.predecessors(stt,label)

    def successors(self,stt,label=None, with_names=False):
        stt = self._find_stt_id_from_stt(stt)
        if with_names:
            return [(sttt,self._states[sttt]) if not self._states[sttt]=="" else sttt 
                     for sttt in self._A.successors(stt,label)]
        else:
            return self._A.successors(stt,label)

    def accepts(self,shuf):
        """
        Takes an instance shuf of shuffle.Shuffle and
        decides whether there's a succesful run 
        with those labels in the spliffer.
        """
        to_treat = self.initial_states()
        for i in to_treat:
            b = self.accepts_from_stt(i,shuf)
            if b:
                return b
        return False
    
    def accepts_from_stt(self,stt,shuf):
        """
        Takes an instance shuf of shuffle.Shuffle and
        decides whether there's a succesful run 
        with those labels in the spliffer starting from
        state stt.
        """
        stt = self._find_stt_id_from_stt(stt)
        if len(shuf) == 0:
            return True if self.is_final(stt) else False
        else:
            to_treat = self.successors(stt,label=shuf.shuf()[0].val)
            for s in to_treat:
                b = self.accepts_from_stt(s,shuf[1:])
                if b:
                    return b
            return False


    def _find_stt_id_from_name(self,name):
        """
        Auxiliary function which returns the number id
        of a spliffer state from its name.
        """
        stt = -1
        for key in self._states.keys():
            if self._states[key]==name:
                stt=key
                break
        if stt >= 0:
            return stt
        else:
            raise ValueError(
                "name does not match any state of Spliffer"
            )
        
    def _find_stt_id_from_stt(self,stt):
        """
        Auxiliary function which returns the number id
        of a spliffer state no matter the input format of that state.
        This is necessary as states can be called in the following ways
        depending on context:
        * (stt_id,stt_name)
        * stt_id
        * stt_name
        """
        
        if isinstance(stt,tuple):
            stt = stt[0]
        elif isinstance(stt,str):
            stt = self._find_stt_id_from_name(stt)
        return stt

    def display(self, horizontal=True):
        self._A.display(horizontal)

