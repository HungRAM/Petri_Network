from string import Template

class Place:
    def __init__(self, token:int = 0, label:str = 'p'):
        self.token = max(token,0)
        self.label = label

    def non_blocking(self)->bool:
        return self.token >= 1

    def trigger(self, state:bool):
        '''
        state = true: place send token to transion
        state = false: place get token from transition
        '''
        if self.token <= 0 and state: return
        self.token -= 1 if state else -1

    def __str__(self):
        log = 'Place \'{}\': {} token'.format(self.label,self.token)
        if self.token >= 2:
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

    def add_P_label(self, labels:list):
        if len(labels) != len(self.P):
            print('Labels length not match')
            return
        for p,l in zip(self.P,labels):
            p.label = l

    def add_T_label(self, labels:list):
        if len(labels) != len(self.T):
            print('Labels length not match')
            return
        for t,l in zip(self.T,labels):
            t.label = l

    def set_marking(self, marking:list):
        if len(marking) != len(self.P):
            return False
        for p,m in zip(self.P,marking):
            p.token = m
        return True

    @property
    def reachable_marking(self):
        init_mark = tuple([p.token for p in self.P])
        marking_set = set()
        marking_set.add(init_mark)
        queue = [init_mark]

        while len(queue) != 0:
            cur_mark = queue[0]
            queue.pop(0)
            self.set_marking(cur_mark)
            for t in self.T:
                if t.is_enable():
                    t.fire()
                    m = tuple([p.token for p in self.P])
                    if m not in marking_set:
                        marking_set.add(m)
                        queue.append(m)
                    self.set_marking(cur_mark)

        self.set_marking(init_mark)
        return list(marking_set)

    def show_reachable_marking(self):
        reach_mar = self.reachable_marking
        print('There are {} reachable marking'.format(len(reach_mar)))
        for m in reach_mar:
            s = '['
            for token,p in zip(m,self.P):
                s += '{}.{}, '.format(token,p.label)
            s = s[:-2]+']'
            print(s)

    def all_firing_sequence(self, filename:str = 'firing_sequence.txt', limit:int = 1000):
        f = open(filename,'w')
        templ_str = Template('Firing sequence: $fs\nMarking: $m\n\n')
        f.write('All firing sequence and marking:\n\n')

        init_mark = [p.token for p in self.P]
        queue = [[[],init_mark]]
        count = 0

        while len(queue) != 0:
            cur_seq,cur_mark = queue[0]
            queue.pop(0)
            f.write(templ_str.substitute(fs=cur_seq,m=cur_mark))
            self.set_marking(cur_mark)
            count+=1
            if count >= limit:
                f.write("To be continued...")
                break
            for t in self.T:
                if t.is_enable():
                    t.fire()
                    m = [p.token for p in self.P]
                    queue.append([cur_seq+[t.label], m])
                    self.set_marking(cur_mark)
        self.set_marking(init_mark)
        print('Open \'{}\' to see the result!'.format(filename))
        f.close()

    def auto_firing(self, limit:int = 100):
        count = 0
        templ_str = Template('\'$t\' fired!\nMarking: $m\n')
        is_deadblock = False
        print('Start {}\n'.format(self.marking))

        while count < limit and not is_deadblock:
            count+=1
            is_deadblock = True
            for t in self.T:
                if t.is_enable():
                    t.fire()
                    is_deadblock = False
                    print(templ_str.substitute(t=t.label,m=self.marking))
                    break
        if is_deadblock:
            print('Deadblock!')
        else:
            print('To be continued...')
            

    def __str__(self):
        ps = [p.label for p in self.P]
        ts = [t.label for t in self.T]
        m = self.marking
        return 'P = {}\nT = {}\nM = {}'.format(ps,ts,m)

    @property
    def marking(self):
        marking = '['
        for p in self.P:
            marking += '{}.{}, '.format(p.token,p.label)
        marking = marking[:-2]+']'
        return marking

    def fire(self, t_index:int):
        if t_index >= len(self.T):
            print('Out of range transition')
            return
        if t_index < 0:
            print('Index must be non-negative')
        t = self.T[t_index]
        t_label = t.label if t.label != 't' else 't{}'.format(t_index)
        if self.T[t_index].fire():
            print('\'{}\' fired'.format(t_label))
        else:
            print('\'{}\' is not enabled'.format(t_label))

    def run(self):
        menu = '''\
MAIN MENU
[1] Set marking
[2] Fire by tripition
[3] Auto fire
[4] Show reachable marking
[5] Show all firing sequence and marking
[6] Exit/Quit'''

        running = True
        while running:
            print(menu)
            ip = input('Enter your choice [1,6]: ').strip()
            while not ip.isdigit() or not (0<=int(ip)<=6):
                ip = input('Wrong menu selection, please try again... ')

            if ip=='1':
                is_valid = False
                new_mark = []
                marking_templ = ""
                for p in self.P:
                    marking_templ += '.{} '.format(p.label)
                print("Enter new marking [ {}]:".format(marking_templ))
                new_mark = input('>> ').strip().split()
                while True:
                    is_valid = True
                    # check valid marking
                    for i in range(len(new_mark)):
                        if new_mark[i].isdigit():
                            new_mark[i] = int(new_mark[i])
                        else:
                            is_valid = False
                            break
                    if len(new_mark) != len(self.P):
                        is_valid = False

                    if is_valid: break
                    print("Marking not match, please try again...")
                    new_mark = input('>> ').strip().split()

                self.set_marking(new_mark)
                print('Current marking: {}'.format(self.marking))

            elif ip=='2':
                print('Fire by transition')
            elif ip=='3':
                print('Auto fire')
            elif ip=='4':
                print('Show reachable marking')
            elif ip=='5':
                print('Show all firing sequence and marking')
            else:
                print('End!')
                running = False
            print()
            

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