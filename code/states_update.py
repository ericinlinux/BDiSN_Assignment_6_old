

'''
Calculates the next time step for the state of the nodes
'''
import numpy as np


'''
The attribute state in every node defines the last state of the node. At the dictionary activityTimeLine we have the
evolution of the values for the state over time.
'''
def states_update(g, t, model='logistic'):
    if t % 10 == 0:
        print t
    g_new = g.copy()
    delta = 1
    speed_factor = 0.3

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





'''
function [ states_new ] = calculate_states(  new_relations, store_states, number_agents, step  )

states_new = zeros(number_agents, 1); %create a new matrix with the state values
update_s = 0.2; % = eta
s = 1; % counter
impact_new = 0;

weight_calculation = new_relations; %temporary used relations
weight_calculation( weight_calculation == 0.1) = 0; %change 0.1 to 0 so the relation value will not be included in the sum

for i = 1:number_agents %for each state
    w(i) = sum(weight_calculation(:,i));
    count_relations = new_relations(:,i).';
    for weight_value = 1:numel(count_relations)
        impact = new_relations(weight_value, i) * store_states(s,step-1); %calculate the impact
        impact_new = impact_new + impact; %sum the impact
        s = s+1;
    end
    s = 1;
    if impact_new > 0 %if impact is greater than 0
        aggimpact = impact_new / w(i); %calculate the aggregated impact
        new_state = store_states(i, step-1) + update_s * (aggimpact - store_states(i, step-1)); %calculate the new state value
        states_new(i,1) = new_state;
    end
    impact_new = 0; %set the impact back to 0
end

end %function
'''