from petri_network import PetriNetwork

marking = [2,0,0]
transitions = {
    't1': [[0],[1]],
    't2': [[1],[2]]
}
t_labels = ['start','change']
p_labels = ['wait','inside','done']

net = PetriNetwork(transitions, marking)
# net.add_P_label(p_labels)
# net.add_T_label(t_labels)
# print(net.marking)
print(net)
# print(net.P[0])
# print(net.T[0])
net.fire(0)
print(net.marking)
net.fire(1)
print(net.marking)