from petri_network import PetriNetwork

marking = [10,10,10,10,10,10]
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
print('All reachable marking: ')
net.show_reachable_marking()