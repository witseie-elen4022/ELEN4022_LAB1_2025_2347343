from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np
import matplotlib.pyplot as plt

def create_fully_connected_circuit(n): #Creates a quantum circuit where every qubit is entangled with every other qubit using CNOT gates
    qc = QuantumCircuit(n)
    for i in range(n):
        for j in range(i + 1, n):
            qc.cx(i, j)
    return qc

def calculate_unitary(qc): #Computes the unitary matrix of a quantum circuit 
    return Operator(qc).data

def apply_cnot(n, control, target, U):  #Applies a CNOT gate on a given number of qubits
    size = 2 ** n
    for i in range(size):
        if ((i >> control) & 1) == 1: 
            j = i ^ (1 << target)  # Flips the target qubit
            U[[i, j]] = U[[j, i]]  # Swap rows
    return U

def calculate_unitary_linear_algebra(n): #Constructs the unitary matrix for a fully connected circuit without large Kronecker products
    U = np.eye(2 ** n, dtype=np.complex128)  # Start with identity matrix
    for i in range(n):
        for j in range(i + 1, n):
            U = apply_cnot(n, i, j, U)  # Apply CNOT directly
    return U

def compare_results(qc, n): #Compares the unitary matrix from Qiskit with the expected linear algebra result
    unitary_qiskit = calculate_unitary(qc)
    unitary_algebra = calculate_unitary_linear_algebra(n)
    match = np.allclose(unitary_qiskit, unitary_algebra)
    return match

def display_circuit(qc): #Displays the quantum circuit diagram
    qc.draw(output='mpl')
    plt.show()

if __name__ == "__main__":
    num_qubits = 5 
    circuit = create_fully_connected_circuit(num_qubits)
    print("Quantum Circuit:")
    print(circuit)
    display_circuit(circuit)
    match = compare_results(circuit, num_qubits)
