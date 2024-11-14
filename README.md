# Deutsch-Jozsa Implementation 
### Running the program 
call ```DJ(n, f)```, where n is the number of qubits in the circut, and f is the encoding of f(x) as a circuit, Uf.
### How to Input f
The user can encode f as a circuit with n+1 qubits, where n is the length of the input bitstring. Then, pass the circuit as the argument f when calling ```DJ```. 

![Image](https://raw.githubusercontent.com/LondonMae/qiskit_algos/main/img/dj_circuit.png)
### Understanding the output
You can run the function with or without noise (ie. ```with_noise=True```). In both cases, DF returns a count map, which maps the output to the number of occurances after 1000 shots through the circuit. In the case with no noise, there is only one element in the count map. The program then plots the counts as a histogram. 

### Running with Noise 
The following histogram is the result of running the program with a noisy simulator:

![Image](https://raw.githubusercontent.com/LondonMae/qiskit_algos/main/img/dj_with_noise.png)

### Change in Execution Time as the Number of Qubits increase
The graph indicates that simon's scales linearly as the number of qubits increase. This makes sense because the runtime of the DJ algorithm is O(n), which is an exponential speedup from the classicial implementation

![Image](https://raw.githubusercontent.com/LondonMae/qiskit_algos/main//img/dj_execution_time.png)

# Grover Implementation
### Running the program 
call ```Grover(n, f)```, where n is the number of qubits in the circut, and f is the encoding of f(x) as a circuit, Zf, which should match the number of qubits n+1, where n is the length of the input bitstring. 
### How to Input f
To encode f, the user should create a circuit with qubits for the every bit in the input bitstring plus one helper qubit. For examply, you can implement the case where the all 0 input outputs 1 with an n-qubit controlled-not gate, followed by a z gate on a helper qubit, followed by the same n-qubit controlled-not gate. By doing this, the circuit flips the phase of the quantum system only if the qubits are set to states that match the bitstring that evaluates to 1 when passed to f. See the example circuit below:  

### Understanding the output
You can run the function with or without noise. In both cases, they return a count map, which maps the output to the number of occurances after 1000 shots through the circuit. In the case with no noise, there is only one element in the count map. The program then plots the counts as a histogram.  

The output should be the bitstring of the input x, such that f(x) = 1. There is a small probability that the output evaluates to a different bitstring.  

### Running with Noise 
You can run the function with or without noise (ie. ```with_noise=True```). In both cases, DF returns a count map, which maps the output to the number of occurances after 1000 shots through the circuit. In the case with no noise, there is only one element in the count map. The program then plots the counts as a histogram. 

### Change in Execution Time as the Number of Qubits increase
The graph indicates that Grover scales exponentially as you increase the number of qubits. This makes sense because the runtime of Grover's algorithm is ```O(sqrt(N))```, where n is ```2**n```. The algorithm is still exponential, with a quadratic speedup. 

