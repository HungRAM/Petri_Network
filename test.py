from petri_network import *

if __name__ == '__main__':
    transitions = {
        't1':[[0],[4]],
        't2':[[1],[4]],
        't3':[[2],[4]],
        't4':[[3],[4]],
    }
    marking = [3,3,3,3,0]
    net = PetriNetwork(transitions, marking)
    run1(net)