from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import GlobalPhaseGate, MCXGate
from math import pi, sqrt
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from noisemodel import construct_bitphaseflip_noise_model
import time

# n is the number of qubits
def DJ(n, f, with_noise = False):

    assert n > 0
    assert f.num_qubits == n + 1

    # A quantum circuit with n+1 qubits, where the last 
    # qubit (n) is a helper qubit
    qc = QuantumCircuit(int(n)+1, int(n)) 

    for i in range(int(n)):
        qc.reset(i)
  
    # barrier between input state and gate operation 
    qc.barrier()
    # Now we've encoded the input, we can run the circuit

    # apply h to upper n qubits
    for i in range(int(n)):
        qc.h(i)

    # set helper qubit to |1> and apply H
    qc.x(int(n))
    qc.h(int(n))

    qc.barrier()
    # this is where we embed Uf
    qc = qc.compose(f)
    qc.barrier()
    
    # apply H to upper n qubits
    for i in range(int(n)):
        qc.h(i)

    qc.barrier()
    
    # measure all qubits except for the helper
    for i in range(int(n)):
        qc.measure(i,int(n)-1-i)

    # We'll run the program on a simulator
    backend = AerSimulator()
    if with_noise:
        noise_model=construct_bitphaseflip_noise_model(0.1,0.1,0.1)
        job = backend.run(qc, shots=1000,noise_model=noise_model) # Run the circuit 1000 times 
       
    else:
        job = backend.run(qc, shots=1, memory=True)

    output = job.result().get_counts() 
    
    return qc, output


def balanced_function(n):
    f = QuantumCircuit(n+1, 0)
    f.cx(0,n)

    return f

def constant_function(n):
    f = QuantumCircuit(n+1, 0)
    f.x(n)
    return f

def plot_qubit_scaling():
    times = []
    for i in range(1, 500):
        t = time.time()

        f = balanced_function(i)
        DJ(i, f, with_noise=False)

        t = time.time() - t
        times.append(t)

    plt.plot(times)
    plt.title("DJ Change in Execution Time with Change in Qubits")
    plt.ylabel("Execution Time")
    plt.xlabel("Number of Qubits")
    plt.show()

# run once
n = 5
f = balanced_function(n)
qc, output = DJ(n, f, with_noise=True)
plot_histogram(output)
print(output)
qc.draw("mpl")
plt.show()

plot_qubit_scaling()



