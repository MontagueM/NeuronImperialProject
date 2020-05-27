from brian2 import *

# Morphology, need to experiment with this to figure out what to do
morphology = Cylinder(length=1*cm, diameter=500*um, n=1, type='axon')

# Our constants for the diff. equations
EL = 10.613*mV
ENa = 115*mV
EK = -12*mV
gL = 0.3*msiemens/cm**2
gNa = 120*msiemens/cm**2
gK = 36*msiemens/cm**2

# Set of equations that will be calculated for HH
eqs = '''
Im = gK * n**4 * (EK-v) + gNa *  m**3* h * (ENa-v) + gL * (EL-v) : amp/meter**2
I : amp (point current) # applied current
dn/dt = alphan * (1-n) - betan * n : 1
dm/dt = alpham * (1-m) - betam * m : 1
dh/dt = alphah * (1-h) - betah * h : 1
# The exprel here is important as otherwise it keeps rounding to zero, exprel keeps precision good for the small nums
alphan = (0.01/mV) * 10*mV/exprel((-v+10*mV)/(10*mV))/ms : Hz
alpham = (0.1/mV) * 10*mV/exprel((-v+25*mV)/(10*mV))/ms : Hz
alphah = 0.07 * exp(-v/(20*mV))/ms : Hz
betan = 0.125*exp(-v/(80*mV))/ms : Hz
betam = 4 * exp(-v/(18*mV))/ms : Hz
betah = 1/(exp((-v+30*mV) / (10*mV)) + 1)/ms : Hz
'''

# Creating the neuron
neuron = SpatialNeuron(morphology=morphology, model=eqs, method="exponential_euler",
                       refractory="m > 0.4", threshold="m > 0.5",
                       Cm=1*uF/cm**2, Ri=35.4*ohm*cm)
# Neuron starting parameters
neuron.v = 0 * mV
neuron.h = 1
neuron.m = 0
neuron.n = .5
neuron.I = 0*amp
state = StateMonitor(neuron, 'v', record=True)

# The actual simulation timings.
'''
1. 50ms of lead-up, init of neuron
2. 1uA current sent through
3. Run sim of that current, simulating a pulse
4. Set the current back to 0
5. Allow refractory period to set in
'''
run(50*ms)
neuron.I = 1*uA # set to I[0] with a higher neuron count and iterate over the plot to get neuron propagation
run(3*ms)
neuron.I = 0*amp
run(50*ms)

# Plotting the graph
print("Plotting graph")
plot(state.t/ms, state.v.T/mV - 70) # -70mV displacement
ylabel('Action potential (V)')
xlabel('Time (ms)')
yticks(np.arange(-80, 35, 5))
show()