from enum import Enum
import random
import sys
# To stop any recursion limits from stopping the simulation from running at high neuron counts
sys.setrecursionlimit(1000000)


class NeuronType(Enum):
    """
    Enum that represents the different types of neuron connection with their respective probability of causing
     subsequent firings.
    """
    EXCITATORY = 0.8
    INHIBITORY = 0.2


class Neuron:
    """
    A class to represent a single neuron.

    ...

    Attributes
    ----------
    number_identifier:
        the number that this specific neuron is in our model to help understand propagation

    Methods
    -------
    f(init, t):
        Stores the equations necessary for solving the differential equations, as well as recording the data
        for graphs.

    run(time_length, current_start):
        Runs the differential equation solver over a specified time period in ms with a specified constant current.

    send_data_forward():
        Sends the last voltage and timestamp we had from this neuron to the next one along to carry on the signal.
        Current just framework as this is not actually how neuron connections work.

    get_data_behind(voltage, last_time):
        Gets the last voltage and timestamp from the neuron connection to start an action potential.
    """

    voltages = []
    timestamps = [0]
    I = 0

    def __init__(self, number_identifier, layer):
        self.forward_connections = {}
        self.number_identifier = number_identifier
        self.layer = layer

    def send_data_forward(self, runtime_ms, stored_data=None):
        """
        Called when we want to progress from this neuron's action potential to our connections. This will propagate
        the timing and voltage info to all the other connections we have, and starting an action potential.
        :return: the data needed for plotting this neuron's graph
        """
        if stored_data is None:
            stored_data = []
        activity_data = []

        # We only want to allow propagations to occur during a specific time period
        if self.timestamps[-1] < runtime_ms:
            # The time to send to our connections as their start time
            call_time = self.timestamps[-1]

            # For every connection we have, try to call them to start their action potential
            for connection, connection_type in self.forward_connections.items():
                # We'll allow a connection if its connection propagation probability is good
                # Sending the call for the connection's action potential
                #random_time = random.random()
                activity_data_add1, num_identifier = connection.get_data_behind(last_time=call_time, stored_data=stored_data)
                activity_data.append([activity_data_add1, num_identifier])
                # the connection type of this connection determines if we actually get anything back
                if random.random() < connection_type.value:
                    # Propagating the signal on
                    # print(f'Propagating signal from {self.number_identifier} of layer {self.layer} to {connection.number_identifier} of layer {connection.layer}')
                    activity_data_add2 = connection.send_data_forward(runtime_ms, stored_data)
                    activity_data += activity_data_add2

        # Sending data back for graph
        return activity_data

    def get_data_behind(self, last_time=0, stored_data=None):
        """
        After this neuron's back-connections are ready to send data, they send data ahead to their connections like this
        call. This uses the data to start a new action potential with the data given and this neuron's settings.
        :param last_time: the last time stamp to use
        :param stored_data: the stored data from the neuron simulation. We need to do this to allow for a large sim
        :return: the data needed for plotting this neuron's graph
        """
        if stored_data is None:
            stored_data = []
        print(f"Getting data for neuron #{self.number_identifier} timestamp {last_time}")
        if stored_data:
            adjusted_stored_timestamps = [x + self.timestamps[-1] for x in stored_data]
            activity_data = stored_data[-1] + last_time
            self.timestamps += adjusted_stored_timestamps
            #print(activity_data)
            return activity_data, self.number_identifier
