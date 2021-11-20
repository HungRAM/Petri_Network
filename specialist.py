from petri_network import *

if __name__ == '__main__':
    # init petri net
    specialist_templ = Template('''
  free                                        docu
  ____                                        ____
 /    \                +----+                /    \ 
(  $free  ) <------------ |    | <------------ (  $docu  )
 \____/                +----+                \____/
   |                     end                   ^
   |                                           |
   |                                           |
   |                    busy                   |
   v                    ____                   |        
 +----+                /    \                +----+
 |    | ------------> (  $busy  ) ------------> |    |
 +----+                \____/                +----+
  start                                      change
''')
    marking = [1,0,0]
    transitions = {
        't1': [[0],[1]],
        't2': [[1],[2]],
        't3': [[2],[0]]
    }
    t_labels = ['start','change','end']
    p_labels = ['free','busy','docu']
    net = PetriNetwork(transitions, marking)
    net.add_P_label(p_labels)
    net.add_T_label(t_labels)

    # 1b i
    # run1(net,specialist_templ,max_token=1)

    # 1b ii
    run1(net,specialist_templ)