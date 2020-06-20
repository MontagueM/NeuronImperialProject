import neuron_efficient as neuron
import neuron as neuron_original
import matplotlib.pyplot as plt
import random
import numpy as np


class MapModel:
    # Array of all our neurons in the model
    neurons = []
    # All the activity calls to show the activity graph
    activity_data = []
    # All stored data. We use this to not have to keep running the simulation every call and instead rely on this data
    # to help with the model.
    stored_timestamps = []

    def __init__(self, runtime_ms, layer_neuron_count, layer_fixed_conn_probs, layer_excitatory_probs, layers):
        self.runtime_ms = runtime_ms
        self.layer_neuron_count = layer_neuron_count
        self.layer_fixed_conn_probs = layer_fixed_conn_probs
        self.layer_excitatory_probs = layer_excitatory_probs
        self.layers = layers  # Array of all possible layers eg [1, 3, 5a]
        self.neuron_layer_dict = {key: [] for key in layers}

    def get_stored_data(self):
        """ Gets all the stored data we need at the beginning of the model simulation """
        test_neuron = neuron_original.Neuron(-1)
        data = test_neuron.get_data_behind()
        # The data from our neuron calculations are 10x the usual scale in order to improve accuracy, need to downscale
        self.stored_timestamps = [x / 10 for x in data]

    def populate_neurons(self):
        """ Appends the neuron array with all the connections it needs """
        layer_to_make_on = 0
        for i in range(sum(list(self.layer_neuron_count.values()))):
            if self.layer_neuron_count[self.layers[layer_to_make_on]] == 0:
                layer_to_make_on += 1
            layer = self.layers[layer_to_make_on]
            self.layer_neuron_count[layer] -= 1
            new_neuron = neuron.Neuron(i, layer)
            self.neurons.append(new_neuron)
            self.neuron_layer_dict[layer].append(new_neuron)
        print([len(x) for x in self.neuron_layer_dict.values()])
        print(len(self.neurons))


    def try_get_layer_connection(self, layer):
        adjusted_layer_fixed_probs = {x:y for x,y in self.layer_fixed_conn_probs.items() if x.split('->')[0] == layer}
        sum_probs = sum(adjusted_layer_fixed_probs.values())
        probability = random.uniform(0, sum_probs)
        t = probability
        connection_layer = -1
        for dict_layer, dict_value in adjusted_layer_fixed_probs.items():
            probability -= dict_value
            if probability <= 0:
                connection_layer = dict_layer
                break
        if connection_layer == -1:
            print('dumb')
            quit()
        return connection_layer.split('->')[-1]

    def populate_neuron_connections(self, n, layer):
        """
        Gives each neuron the connections given the constants provided
        :param n: the neuron to add the connections to
        """
        forward_connections = {}
        # We don't want to connect to ourselves
        neurons_wo = list(self.neurons)
        neurons_wo.remove(n)

        for layer_exchange, f_percent in self.layer_fixed_conn_probs.items():
            if layer_exchange.split('->')[0] == layer:
                # print(f'neuron {n.number_identifier} layerexc {layer_exchange} fperc {f_percent} no. {round(f_percent * len(self.neuron_layer_dict[layer]))}')
                for i in range(round(f_percent * len(self.neuron_layer_dict[layer]))):
                    layer_to_connect_to = layer_exchange.split('->')[1]
                    random_index = random.randint(0, len(self.neuron_layer_dict[layer_to_connect_to]) - 1)
                    connecting_neuron = self.neuron_layer_dict[layer_to_connect_to][random_index]
                    # We are now connecting to a neuron in this chosen layer
                    if random.random() < self.layer_excitatory_probs[layer]:
                        connection_type = neuron.NeuronType.EXCITATORY
                    else:
                        connection_type = neuron.NeuronType.INHIBITORY
                    # print(connecting_neuron.number_identifier)
                    forward_connections[connecting_neuron] = connection_type
        n.forward_connections = forward_connections
        # print(f'neuron {n.number_identifier} no. forward {len(n.forward_connections)}')
        ####
        # number_of_connections = round(len(self.neurons)*0.10)
        # for i in range(number_of_connections):
        #     layer_to_connect_to = self.try_get_layer_connection(layer)
        #     # print(layer_to_connect_to)
        #     random_index = random.randint(0, len(self.neuron_layer_dict.values())-1)
        #     connecting_neuron = self.neuron_layer_dict[layer_to_connect_to][random_index]
        #     # We are now connecting to a neuron in this chosen layer
        #     if random.random() < self.layer_excitatory_probs[layer]:
        #         connection_type = neuron.NeuronType.EXCITATORY
        #     else:
        #         connection_type = neuron.NeuronType.INHIBITORY
        #     forward_connections[connecting_neuron] = connection_type
            # if n.number_identifier == 0:
            #     print(f'Adding forward connection of type {connection_type} to {connecting_neuron.number_identifier} from {n.number_identifier}')
        # n.forward_connections = forward_connections

    def propagate(self):
        """ This code makes every neuron, assigns all connections, and starts signal propagation. """
        # Appends the neuron array with all the connections it needs
        self.populate_neurons()

        # Gives each neuron the connections given the constants provided
        for layer, neurons in self.neuron_layer_dict.items():
            """
            We want 10% connectivity with the whole population so 10% of total count and randomly choose from array??
            """
            for neuron in neurons:
                self.populate_neuron_connections(neuron, layer)
        # neuron_start_index = random.randint(0, len(self.neurons)-1)
        neuron_start_index = 2500
        start_neuron = self.neurons[neuron_start_index]
        print(f"going to start propagation with id {start_neuron.number_identifier} of layer {start_neuron.layer} and # of forward connections {len(start_neuron.forward_connections)}")
        # Starts the propagation
        print(self.neurons[neuron_start_index].forward_connections)
        print(len(self.neurons))
        activity_data_add = start_neuron.send_data_forward(runtime_ms=self.runtime_ms,
                                                              stored_data=self.stored_timestamps)
        self.activity_data += activity_data_add

    def run_model(self):
        self.get_stored_data()

        # Running our model for RUNTIME_MS ms
        self.propagate()

        activity_set, activity_y = self.get_activity_axes()

        return activity_set, activity_y
        #self.write_data(activity_set, activity_y)
        #self.plot_activity_graph(activity_set, activity_y)

    def get_activity_axes(self):
        # Counting the number of times spikes occur for a unit of time

        # For numerical we don't need these
        self.activity_data = [x[0] for x in self.activity_data]
        activity_set = list(set(self.activity_data))
        activity_y = [0] * len(activity_set)
        for i, d in enumerate(self.activity_data):
            activity_y[activity_set.index(d)] += 1

        # We need to sort the data by timestamp for a line plot to look correct
        return zip(*sorted(zip(activity_set, activity_y)))

    def write_data(self, activity_set, activity_y):
        # Writing the data for permanent storage
        with open('activity.txt', 'a') as f:
            f.write(
                f"\n\n{activity_set}\n{activity_y}\nRUNTIME_MS {self.runtime_ms} TOTAL_NEURON_COUNT {self.total_neuron_count} EXCITE_PROB {self.excitatory_probability}")

    def plot_activity_graph(self, x, y):
        # Plotting the data
        plt.plot([x * 1 for x in x], y,
                 label=f"RUNTIME_MS {self.runtime_ms} TOTAL_NEURON_COUNT {self.total_neuron_count} EXCITE_PROB {self.excitatory_probability}")
        plt.xlabel("Time [ms]")
        plt.ylabel("Count per unit time")
        plt.legend()