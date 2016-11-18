

'''
Calculates the next time step for the state of the nodes
'''
import numpy as np


'''
The attribute state in every node defines the last state of the node. At the dictionary activityTimeLine we have the
evolution of the values for the state over time.
'''
def edges_update(graph, t, model='original'):
    if t % 10 == 0:
        print t

    g = graph.copy()
    delta = 1
    speed_factor = 0.2
    thres_h = 0.1


    for edge in g.edges():
        source, target = edge
        old_weight = g.get_edge_data(source,target).values()[0]['weight']
        state_source = g.node[source]['state']
        state_target = g.node[target]['state']

        new_weight = old_weight + speed_factor * (old_weight * (1 - old_weight)) * (thres_h - abs(state_source - state_target))*delta # homophily model

        g[source][target]['weightTimeLine'].update({t:new_weight})
        g[source][target][0]['weight'] = new_weight

    return g


'''
        if aggimpact > 0:
            # new_state = store_states(i, step-1) + update_s * (aggimpact - store_states(i, step-1)); %calculate the new state value
            old_activity = g.node[node]['state']
            num_neighbours = len(g.neighbors(node))
            # Definition of the speed factor
            if model == 'original':
                new_activity = old_activity + speed_factor * (aggimpact - old_activity) * delta
            elif model == 'weighted':
                if num_neighbours == 0:
                    new_activity = old_activity
                else:
                    new_activity = old_activity + (speed_factor / num_neighbours) * (aggimpact - old_activity) * delta
            elif model == 'logistic':
                new_activity = old_activity + logistic(speed_factor) * (aggimpact - old_activity) * delta
            else:
                print 'Wrong value for model!'
                raw_input()
            g_new.node[node]['activityTimeLine'].update({t: new_activity})
            g_new.node[node]['state'] = new_activity
    return g_new
'''

"""
The logistic function can be tuned by changing the steepness and threshold values. It receives a number and returns a
value between 0 and 1.
"""
def logistic(number):
    steepness = 0.3
    threshold = 10
    log_number = (1 / (1 + np.exp(-steepness * (number - threshold))) - 1 / (1 + np.exp(steepness * threshold))) * \
                (1 + np.exp(-steepness * threshold))
    return log_number
