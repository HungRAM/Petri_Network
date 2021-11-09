class Place:
    def __init__(self, token:int = 0, label:str = 'p'):
        self.__token = max(token,0)
        self.label = label

    @property
    def holding(self)->int:
        return self.__token

    def non_blocking(self)->bool:
        return self.__token >= 1

    def trigger(self, state:bool)->bool:
        '''
        state = true: place send token to transion
        state = false: place get token from transition
        '''
        if self.__token <= 0 and state: return
        self.__token -= 1 if state else -1

    def __str__(self):
        log = 'Place \'{}\': {} token'.format(self.label,self.__token)
        if self.__token >= 2:
            log += 's'
        return log
    
    @classmethod
    def create_n(cls, size, marking:list=[]):
        if size <= 0: return
        if size > len(marking):
            marking += [0]*(size-len(marking))
        labels = ['p{}'.format(i) for i in range(size)]
        ps = []
        for i in range(size):
            ps.append(cls(marking[i],labels[i]))
        return ps


class Transition:
    def __init__(self, label:str = 't'):
        self.__preset = []
        self.__postset = []
        self.label = label

    def add_preset(self,place):
        self.__preset.append(place)

    def add_postset(self,place):
        self.__postset.append(place)

    def is_enable(self):
        return all([p.non_blocking() for p in self.__preset])

    def fire(self):
        flag = self.is_enable()
        if self.is_enable():
            for p in self.__preset:
                p.trigger(True)
            for p in self.__postset:
                p.trigger(False)
        return flag

    def __str__(self):
        return 'Transision \'{}\': {} in, {} out'.format(
            self.label, len(self.__preset), len(self.__postset)
        )
    
    @classmethod
    def create_with_set(cls, preset:list, postset:list, label:str = ''):
        t = cls(label)
        for p in preset:
            t.add_preset(p)
        for p in postset:
            t.add_postset(p)
        return t


class PetriNetwork:
    def __init__(self, transitions:dict, marking:list):
        self.P = Place.create_n(len(marking),marking)
        self.T = []
        for key,val in transitions.items():
            preset = [self.P[i] for i in val[0]]
            postset = [self.P[i] for i in val[1]]
            t = Transition.create_with_set(preset, postset, key)
            self.T.append(t)

    def add_P_label(self, labels):
        if len(labels) != len(self.P):
            print('Labels length not match')
            return
        for p,l in zip(self.P,labels):
            p.label = l

    def add_T_label(self, labels):
        if len(labels) != len(self.T):
            print('Labels length not match')
            return
        for t,l in zip(self.T,labels):
            t.label = l

    def __str__(self):
        ps = [p.label for p in self.P]
        ts = [t.label for t in self.T]
        m = self.marking
        return 'P = {}\nT = {}\nM = {}'.format(ps,ts,m)

    @property
    def marking(self):
        marking = '['
        for p in self.P:
            marking += '{}.{}, '.format(p.holding,p.label)
        marking = marking[:-2]+']'
        return marking

    def fire(self, t_index):
        if t_index >= len(self.T):
            print('Out of range transition')
            return
        t = self.T[t_index]
        t_label = t.label if t.label != 't' else 't{}'.format(t_index)
        if self.T[t_index].fire():
            print('\'{}\' fired'.format(t_label))
        else:
            print('\'{}\' is not enabled'.format(t_label))


if __name__ == '__main__':
    # sample input
    marking = [1,0,0]
    transitions = {
        't1': [[0],[1]],
        't2': [[1],[2]]
    }
    t_labels = ['start','change']
    p_labels = ['wait','inside','done']

    net = PetriNetwork(transitions, marking)
    net.add_P_label(p_labels)
    net.add_T_label(t_labels)
    print(net.marking)