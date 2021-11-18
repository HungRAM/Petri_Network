from petri_network import *

def run(net):
        menu = '''\
MAIN MENU
[1] Set marking
[2] Fire by transition
[3] Auto fire
[4] Exit/Quit'''

        running = True
        while running:
            print(menu)
            print('Current marking: {}'.format(net.marking))
            ip = input('Enter your choice [1,4]: ').strip()
            while not ip.isdecimal() or not (0<=int(ip)<=4):
                ip = input('Wrong menu selection, please try again... ')

            if ip=='1':
                is_valid = False
                new_mark = []
                marking_templ = ""
                for p in net.P:
                    marking_templ += '.{} '.format(p.label)
                print("Enter new marking [ {}]:".format(marking_templ))
                new_mark = input('>> ').strip().split()
                while True:
                    is_valid = True
                    # check valid marking
                    for i in range(len(new_mark)):
                        if new_mark[i].isdecimal():
                            new_mark[i] = int(new_mark[i])
                        else:
                            is_valid = False
                            break
                    if len(new_mark) != len(net.P):
                        is_valid = False

                    if is_valid: break
                    print("Marking not match, please try again...")
                    new_mark = input('>> ').strip().split()

                net.set_marking(new_mark)
                print('Current marking: {}'.format(net.marking))

            elif ip=='2':
                t_label = ' '
                for t in net.T:
                    t_label += t.label + ' '
                print('\nEnter X to exit')
                print('Transition list: [{}]'.format(t_label))
                while True:
                    t_idx = input('\nEnter transition\'s index [0,{}]: '.format(len(net.T)-1)).strip()
                    if t_idx.lower() == 'x':
                        break
                    if not t_idx.isdecimal():
                        print('Index must be a number!')
                        continue
                    t_idx = int(t_idx)
                    if not (0 <= t_idx < len(net.T)):
                        print('Index is out of range [0,{}]'.format(len(net.T)-1))
                        continue
                    net.fire(t_idx)

            elif ip == '3':
                print('Auto fire will start after 3s')
                print('Press P to pause')
                time.sleep(0.5)
                for i in range(3):
                    print(str(3-i), end=' ')
                    time.sleep(1)
                print('Lets\'go')
                net.auto_firing()
                sys.stdout.flush()
                while msvcrt.kbhit():
                    msvcrt.getch()
            
            else:
                print('Goodbye<3')
                running = False
            print()

if __name__ == '__main__':
    marking = [5,0,1]
    transitions = {
        't1': [[0],[1]],
        't2': [[1],[2]],
    }
    t_labels = ['start','change']
    p_labels = ['wait','inside','done']

    net = PetriNetwork(transitions, marking)
    net.add_P_label(p_labels)
    net.add_T_label(t_labels)

    run(net)