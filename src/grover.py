from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import GlobalPhaseGate, MCXGate
from math import pi, sqrt
from qiskit.visualization import plot_histogram
from noisemodel import construct_bitphaseflip_noise_model
import matplotlib.pyplot as plt
import time

def Z0(n):
    assert n > 0
    """ creates a curcuit that flips the phase if 
        the non-helper qubits are all 0's """
    z0 = QuantumCircuit(n+1, 0)
    z0.x([i for i in range(n)])
    z0.mcx([i for i in range(n)], n)
    z0.z(n)
    z0.mcx([i for i in range(n)], n)
    z0.x([i for i in range(n)])

    return z0



# n is the number of qubits
def Grover(n, f, with_noise = False):
    assert n > 0

    z0 = Z0(n)

    # A quantum circuit with n+1 qubits, where the last 
    # qubit (n) is a helper qubit
    qc = QuantumCircuit(int(n)+1, int(n)) 

    for i in range(int(n)):
        qc.reset(i)
  
    # barrier between input state and gate operation 
    qc.barrier()
    
    # After encoding input, apply h to all non-helper qubits
    for i in range(int(n)):
        qc.h(i)

    # this tells us how manny times to run G
    k = round(pi*sqrt(2**n)/4 - 1/2)

    # passes through circuit (G) k times
    for _ in range(k):
        qc.barrier()
        # encoding of Zf
        qc = qc.compose(f)
        
        # apply hadamard to upper n qubits
        for i in range(int(n)):
            qc.h(i)
        
        # encoding of z0, so flip phase if 
        # qubits are are 0's
        qc = qc.compose(z0)

        # apply hadamard to upper n qubits again
        for i in range(int(n)):
            qc.h(i)

        # this flips the phase of the circuit (encode the minus sign)
        qc.x(n)
        qc.z(n)
        qc.x(n)

    qc.barrier()
    
    # measure upper-n qubits and reverse order in register
    for i in range(int(n)):
        qc.measure(i,int(n)-1-i)


    # We'll run the program on a simulator
    backend = AerSimulator()
 
    
    if with_noise:
        noise_model=construct_bitphaseflip_noise_model(0.1,0.1,0.1)
        job = backend.run(qc, shots=1000,noise_model=noise_model) # Run the circuit 1000 times 
       
    else:
        job = backend.run(qc, shots=1, memory=True)

    print(job.result())
    output = job.result().get_counts() 

    
    return qc, output


def all_one_f(n):
    """ encodes Zf such that f(111...1) is 1
        and all other inputs result in 0 when 
        given as input to f     
    """
    f = QuantumCircuit(n+1, 0)
    f.mcx([i for i in range(n)],n)
    f.z(n)
    f.mcx([i for i in range(n)],n)

    return f

def plot_qubit_scaling():
    times = []
    for i in range(1, 20):
        t = time.time()

        f = all_one_f(i)
        Grover(i, f, with_noise=False)

        t = time.time() - t
        times.append(t)

    plt.plot(times)
    plt.title("Grover Change in Execution Time with Change in Qubits")
    plt.ylabel("Execution Time")
    plt.xlabel("Number of Qubits")
    plt.show()

# run once
n = 2
f = QuantumCircuit(n+1, 0)
f.x(0)
f.x(2)
f.mcx([i for i in range(n)],n)
f.z(n)
f.mcx([i for i in range(n)],n)
f.x(0)
f.x(2)

qc, output = Grover(n, f, with_noise=True)
# plot_histogram(output)
print(output)
qc.draw("mpl")
plt.show()

plot_qubit_scaling()





