'''
Calculates the next time step for the state of the nodes
'''
import numpy as np


'''
The attribute state in every node defines the last state of the node. At the dictionary activityTimeLine we have the
evolution of the values for the state over time.
'''
def edges_update(graph, t, function='original', delta = 1, speed_factor = 0.2, thres_h = 0.1, persistence=None, amplification=None):
    edges_functions = ['hebbian', 'simple_linear', 'advanced_linear', 'simple_quadratic', 'advanced_quadratic']

    if t % 10 == 0:
        print t

    g = graph.copy()

    for edge in g.edges():
        source, target = edge
        old_weight = g.get_edge_data(source,target).values()[0]['weight']
        state_source = g.node[source]['state']
        state_target = g.node[target]['state']

        variation = 0
        if function == 'hebbian':
            if persistence == None:
                print 'Error! Give persistence value to calculate hebbian operations!'
                exit(0)
            else:
                variation = speed_factor * (source * target * (1 - target) + persistence * target)

        elif function == 'simple_linear':
            if amplification == None:
                print 'Error! Amplification not set!'
                exit(0)
            else:
                variation = amplification * old_weight * (1 - source) * (thres_h - np.abs(source - target))

        elif function == 'advanced_linear':
            if amplification == None:
                print 'Error! Amplification not set!'
                exit(0)

            variation = (old_weight + amplification * ((1 - old_weight) * (np.abs(thres_h - np.abs(source - target))+(
                thres_h - np.abs(source - target))) / 2 + old_weight * (np.abs(thres_h- np.abs(source - target))-(
                thres_h - np.abs(source - target))) / 2))

        elif function == 'simple_quadratic':
            if amplification == None:
                print 'Error! Amplification not set!'
                exit(0)

            variation = (old_weight + amplification * old_weight * (1 - old_weight) * (thres_h^ 2 - np.abs(source - target) ^ 2))

        elif function == 'advanced_quadratic':
            if amplification == None:
                print 'Error! Amplification not set!'
                exit(0)

            variation = (old_weight + amplification * ((1 - old_weight) * (np.abs(thres_h^2 - np.abs(source - target)^2) + (
            thres_h ^ 2 - np.abs(source - target) ^ 2)) / 2 + old_weight * (np.abs(thres_h ^ 2 - np.abs(source - target) ^ 2) - (
                                                           thres_h ^ 2 - np.abs(source - target) ^ 2)) / 2))


        new_weight = old_weight + speed_factor * (variation - old_weight )*delta # homophily model

        g[source][target]['weightTimeLine'].update({t:new_weight})
        g[source][target][0]['weight'] = new_weight

    return g