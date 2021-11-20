from petri_network import *

if __name__ == '__main__':
    merge_templ = Template('''
                        free                                        docu
                        ____                                        ____
                       /    \                +----+                /    \ 
                      (  $free  ) <------------ |    | <------------ (  $docu  )
                       \____/                +----+                \____/
                         |                     end                   ^
                         |                                           |
  wait                   |                   inside                  |                    done
  ____                   v                    ____                   |                    ____
 /    \                +----+                /    \                +----+                /    \ 
(  $wait  ) ------------> |    | ------------> (  $inside  ) ------------> |    | ------------> (  $done  )
 \____/                +----+                \____/                +----+                \____/ 
                        start                                      change
                           -\                                       /^
                              -\                                 /-
                                 -\           busy            /-                       
                                    -\        ____         /-
                                       -\    /    \     /-
                                          ->(  $busy  ) /-
                                             \____/
''')
    marking = [4,1,0,0,1,0]
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

    run3(net,merge_templ)