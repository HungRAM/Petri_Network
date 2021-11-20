from petri_network import *

if __name__ == '__main__':
    patiens_templ = Template('''
  wait                                       inside                                       done
  ____                                        ____                                        ____
 /    \                +----+                /    \                +----+                /    \ 
(  $wait  ) ------------> |    | ------------> (  $inside  ) ------------> |    | ------------> (  $done  )
 \____/                +----+                \____/                +----+                \____/ 
                        start                                      change
''')
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

    run2(net,patiens_templ)