from petri_network import PetriNetwork

marking = [2,2,0,0,0,0]
transitions = {
    't1': [[0,1],[2,3]],
    't2': [[2,3],[4,5]],
    't3': [[5],[1]]
}
t_labels = ['start','change','end']
p_labels = ['wait','free','inside','busy','done','docu']

net = PetriNetwork(transitions, marking)
net.add_P_label(p_labels)
net.add_T_label(t_labels)
# print(net.marking)
# print(net)
# # print(net.P[0])
# # print(net.T[0])
# net.show_reachable_marking()
net.all_firing_sequence('firing_sequence.txt')
net.auto_firing()