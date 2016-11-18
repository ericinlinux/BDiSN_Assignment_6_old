

'''
Calculates the next time step for the state of the nodes
'''
import numpy as np


'''
The attribute state in every node defines the last state of the node. At the dictionary activityTimeLine we have the
evolution of the values for the state over time.
'''
def states_update(g, t, model='logistic', speed_factor = 0.3, delta = 1):
    if t % 10 == 0:
        print t

    g_new = g.copy()

    # Updating the state of each node in the graph
    for node in g.nodes():
        aggimpact = 0
        sum_weights = 0
        # Calculate the agregated impact from the neighbours, together with the sum of the weights.
        for neigh in g.neighbors(node):
            #connect = g.get_edge_data(neigh, node)['weight']
            connect = g.get_edge_data(neigh, node).values()[0]['weight']
            sum_weights = sum_weights + connect
            try:
                aggimpact = aggimpact + g.node[neigh]['activityTimeLine'][t-1]*connect
            except:
                print t, neigh
                exit(0)

        aggimpact = aggimpact/sum_weights

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
        else:
            actual_state = g_new.node[node]['state']
            g_new.node[node]['activityTimeLine'].update({t: actual_state})
    return g_new


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

