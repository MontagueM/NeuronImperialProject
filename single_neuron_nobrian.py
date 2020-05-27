import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.special import exprel


class Neuron:
    def __init__(self):
        # Our constants for the diff. equations
        self.EL = 10.613
        self.ENa = 115
        self.EK = -12
        self.gL = 0.3
        self.gNa = 120
        self.gK = 36

        # Initial conditions
        self.v = 0
        self.h = 1
        self.m = 0
        self.n = .5
        self.C = 1e-6
        self.R = 35.4
        self.varr = None
        self.tarr = [0]

    def f_alphan(self, v):
        return 0.01 * 10 / exprel((-v + 10) / 10)

    def f_alpham(self, v):
        return 0.1 * 10 / exprel((-v + 25) / 10)

    def f_alphah(self, v):
        return 0.07 * np.exp(-v / 20)

    def f_betan(self, v):
        return 0.125 * np.exp(-v / 80)

    def f_betam(self, v):
        return 4 * np.exp(-v / 18)

    def f_betah(self, v):
        return 1 / (np.exp((-v + 30) / 10) + 1)

    def f(self, init, t):
        n = init[0]
        m = init[1]
        h = init[2]
        v = init[3]

        dndt = self.f_alphan(v) * (1 - n) - self.f_betan(v) * n
        dmdt = self.f_alpham(v) * (1 - m) - self.f_betam(v) * m
        dhdt = self.f_alphah(v) * (1 - h) - self.f_betah(v) * h
        dvdt = (1/self.C) * (self.I + self.gK * n**4 * (self.EK-v) + self.gNa * m**3 * h * (self.ENa-v) + self.gL * (self.EL-v))
        self.n = n
        self.m = m
        self.h = h
        self.v = v
        self.varr.append(v)
        self.tarr.append(t)
        return [dndt, dmdt, dhdt, dvdt]

    def run(self, time_length, current_start):
        new_start_time = int(np.floor(self.tarr[-1]))
        print(new_start_time)
        time_region = np.linspace(new_start_time, new_start_time + time_length, 1000).tolist()
        self.varr = [self.v]
        self.tarr = [time_region[0]]
        self.I = current_start

        odeint(self.f, [self.n, self.m, self.h, self.v], time_region)
        return self.varr, self.tarr

    def plot_graph(self, time_points, array):
        plt.plot(time_points, array, 'b', linewidth=1.5)
        plt.xlabel('Time (ms)')
        plt.ylabel('Action potential (mV)')
        plt.show()


neuron = Neuron()
time_sets = [np.linspace(0, 50, 1000).tolist(), np.linspace(50, 53, 1000).tolist(), np.linspace(53, 100, 1000).tolist()]
run1, tarr1 = neuron.run(50, 0)
run2, tarr2 = neuron.run(3, 1)
run3, tarr3 = neuron.run(50, 0)

neuron.plot_graph(tarr1 + tarr2 + tarr3, [x - 70 for x in run1 + run2 + run3])
