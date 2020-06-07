import numpy as np
from scipy.integrate import odeint
from enum import Enum
import random
from map_connections_model import RUNTIME_MS
import sys
import time
# To stop any recursion limits from stopping the simulation from running at high neuron counts
sys.setrecursionlimit(1000000)

#####################################################################

# Definitions of the required variables with respect to voltage. Numbers taken from paper below.
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/?page=19 page 518


def f_alphan(v):
    return 0.01 * (v + 55) / (1 - (np.exp(-(v + 55) / 10)))


def f_betan(v):
    return 0.125 * np.exp(-(v + 65) / 80)


def f_alpham(v):
    return 0.1 * (v + 40) / (1 - (np.exp(-(v + 40) / 10)))


def f_betam(v):
    return 4 * np.exp(-(v + 65) / 18)


def f_alphah(v):
    return 0.07 * np.exp(-(v + 65) / 20)


def f_betah(v):
    return 1 / (1 + np.exp(-(v + 35) / 10))


#####################################################################

class NeuronType(Enum):
    """
    Enum that represents the different types of neuron with their respective probability of causing subsequent firings.
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
    # Our constants for the diff. equations
    EL = -54.4
    ENa = 50
    EK = -70
    gL = 0.3
    gNa = 120
    gK = 36

    # Initial conditions
    v = -62
    h = 0
    m = 0
    n = 0.5
    C = 1e-6

    voltages = []
    timestamps = [0]
    I = 0
    fire_time = 1e9

    def __init__(self, number_identifier):
        self.forward_connections = []
        self.number_identifier = number_identifier

    def f(self, init, t):
        """
        The main function we are integrating over with odeint. odeint solvs the four DEs below, solving them
        and then those results being used for the next solutions (n, m, h, v)

        :param init: an array of the four initial conditions for n, m, h, and v
        :param t: the time instant this solution is being made for
        :return: the four functions odeint will solve
        """
        self.n = init[0]
        self.m = init[1]
        self.h = init[2]
        self.v = init[3]

        # The differential equations that will be solved
        dndt = f_alphan(self.v) * (1 - self.n) - f_betan(self.v) * self.n
        dmdt = f_alpham(self.v) * (1 - self.m) - f_betam(self.v) * self.m
        dhdt = f_alphah(self.v) * (1 - self.h) - f_betah(self.v) * self.h
        dvdt = (1/self.C) * (self.I + self.gK * self.n**4 * (self.EK-self.v) +
                             self.gNa * self.m**3 * self.h * (self.ENa-self.v) + self.gL * (self.EL-self.v))

        # Recording the data the sim has calculated (could do directly but seems to be messy)
        self.voltages.append(self.v)
        self.timestamps.append(t)

        return [dndt, dmdt, dhdt, dvdt]

    def run(self, time_length, current_start):
        """
        Runs the differential equation solver over a specified time period in ms with a specified constant current.

        :param time_length: the length of time to run the simulation for
        :param current_start: the current the simulation will run with over the time period
        :return: two arrays of voltages and timestamps as calculated by the simulation
        """
        # We want each successive run() to start from the last simulation timestamp so it looks continuous.
        new_start_time = np.floor(self.timestamps[-1])

        # Temporary fix for misalignment
        if new_start_time == 50:
            new_start_time += 1

        time_region = np.linspace(new_start_time, new_start_time + time_length, 1000).tolist()

        # Initialising the recording system
        self.voltages = [self.v]
        self.timestamps = [time_region[0]]  # Defining where we want to start with our timestamps

        self.I = current_start

        # The actual differential equation solving
        odeint(self.f, [self.n, self.m, self.h, self.v], time_region)
        return self.voltages, self.timestamps

    def send_data_forward(self, stored_data=None):
        """
        Called when we want to progress from this neuron's action potential to our connections. This will propagate
        the timing and voltage info to all the other connections we have, and starting an action potential.
        :return: the data needed for plotting this neuron's graph
        """
        if stored_data is None:
            stored_data = []
        activity_data = []

        # We only want to allow propagations to occur during a specific time period
        if self.timestamps[-1] < RUNTIME_MS:
            # The time to send to our connections as their start time
            call_time = self.timestamps[-1]

            # For every connection we have, try to call them to start their action potential
            for connection, connection_type in self.forward_connections.items():
                # We'll allow a connection if its connection propagation probability is good

                # Sending the call for the connection's action potential
                # activity_data_add1 = connection.get_data_behind(last_time=call_time, stored_data=stored_data)
                # activity_data.append(activity_data_add1)
                if random.random() < connection_type.value:
                    # AND if it hasn't fired in the last 2ms (hyperpolarisation time)

                    if (time.time() - self.fire_time) > 2e-3:
                        # Sending the call for the connection's action potential
                        activity_data_add1 = connection.get_data_behind(last_time=call_time, stored_data=stored_data)
                        activity_data.append(activity_data_add1)

                        # Propagating the signal on
                        activity_data_add2 = connection.send_data_forward(stored_data)
                        activity_data += activity_data_add2
                    else:
                        print(f"Rejecting call for neuron #{self.number_identifier} as {(time.time() - self.fire_time)} < {2e-3}")


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
        if self.number_identifier == -1:

            # Instantiating the new start values
            self.timestamps[-1] = last_time

            # Running action potential
            run1 = []
            timestamps1 = []
            testv = self.v
            trigger_time_ms = 10
            # If activation const is not high enough the neuron will fail to fire
            activation_const = 2
            for i in range(100):
                # Run normally
                if i > trigger_time_ms:
                    # choosing sine was just an option to make it able to fail by falling back down.
                    testv += np.sin(np.pi / 12 * (i - trigger_time_ms)) * activation_const

                    """-62 is the base potential for the membrane. If the activation potential after trigger time does not cause
                    the action potential and comes back down (as sinusoidal) then it gets stopped at -62. This is very technically
                    inaccurate but it makes a good looking signal."""
                    if testv <= -62:
                        break
                self.run(1, 0)
                run1.append(testv)
                timestamps1.append(last_time + i)
                if testv > -55:
                    self.v = testv
                    run2, timestamps2 = self.run(3, 1)
                    run2 = [x + 10 for x in run2]
                    break
                else:
                    run2, timestamps2 = [], []
            run3, timestamps3 = self.run(30, 0)
            run2, timestamps2 = run2[200:], timestamps2[200:]
            activity_data = timestamps2[-1]
            # Sending data back for graph
            return [[timestamps1 + timestamps2 + timestamps3, run1 + run2 + run3, self.number_identifier]], activity_data, timestamps2
        else:
            if stored_data:
                adjusted_stored_timestamps = [x + self.timestamps[-1] for x in stored_data[0]]
                activity_data = stored_data[1][-1] + last_time
                self.timestamps += adjusted_stored_timestamps
                self.fire_time = time.time()
                return activity_data
            print("No data")
            return [[]], None
