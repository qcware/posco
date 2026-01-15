from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np


def QNP_PX_GATE(theta):

    pi = np.pi

    # Create a 4-qubit quantum circuit for the custom gate
    qnp_px = QuantumCircuit(4)

    #Implementation of the QNP_PX(theta) gate
    qnp_px.cx(3, 1)

    qnp_px.cx(3, 0)

    qnp_px.h(3)
    qnp_px.s(1)
    qnp_px.rz(pi/-2, 0)

    qnp_px.cx(1, 0)
    qnp_px.cx(3, 2)

    qnp_px.rz(pi/2, 0)
    qnp_px.ry(theta/8, 2)
    qnp_px.ry(theta/-8, 3)

    qnp_px.cz(0, 3)

    qnp_px.cx(0, 2)

    qnp_px.ry(theta/-8, 3)
    qnp_px.ry(theta/8, 2)

    qnp_px.cx(1, 2)

    qnp_px.cx(1, 3)

    qnp_px.rz(pi/2, 1)
    qnp_px.ry(theta/-8, 2)
    qnp_px.ry(theta/8, 3)

    qnp_px.cx(0, 2)

    qnp_px.cz(0, 3)

    qnp_px.ry(theta/-8, 2)
    qnp_px.ry(theta/8, 3)

    qnp_px.cx(3, 2)

    qnp_px.h(3)

    qnp_px.cx(3, 1)

    qnp_px.s(3)

    qnp_px.rz(pi/-2, 1)

    qnp_px.cx(1, 0)

    # Convert the circuit to a gate
    # qnp_px_gate = qnp_px.to_gate(label="QNP_PX")

    return qnp_px.to_gate(label="QNP_PX")


def QNP_OR_GATE(phi):

    # Create a 4-qubit quantum circuit for the custom gate
    qnp_or = QuantumCircuit(4)

    #Implementation of the QNP_OR(phi) gate
    qnp_or.h(0)
    qnp_or.h(1)

    qnp_or.cx(0,2)

    qnp_or.cx(1,3)

    qnp_or.ry(phi/2, 0)
    qnp_or.ry(phi/2, 1)
    qnp_or.ry(phi/2, 2)
    qnp_or.ry(phi/2, 3)

    qnp_or.cx(1,3)

    qnp_or.cx(0,2)

    qnp_or.h(1)
    qnp_or.h(0)

    # Convert the circuit to a gate
    # qnp_or_gate = qnp_or.to_gate(label="QNP_OR")

    return qnp_or.to_gate(label="QNP_OR")

def count_QNP_params(n_qbits, n_layers):
   
    n_theta = 0
    n_phi = 0
    for nl in range(2*n_layers):
        ngate = (n_qbits // 4) if nl % 2 == 0 else ((n_qbits - 1) // 4)
        qbit_start = 0  if nl % 2 == 0 else (n_qbits % 4 if n_qbits % 2 != 0 else 2)

        for ng in range(ngate):

            n_theta+=1
            n_phi+=1
            qbit_start+=4

    return n_theta, n_phi

def QNP_fabric(qnp_circuit, n_layers, theta_vect, phi_vect):

    n_qbits = qnp_circuit.num_qubits
    iparam = 0

    for nl in range(2*n_layers):
        ngate = (n_qbits // 4) if nl % 2 == 0 else ((n_qbits - 1) // 4)
        qbit_start = 0  if nl % 2 == 0 else (n_qbits % 4 if n_qbits % 2 != 0 else 2)

        for ng in range(ngate):

            qnp_circuit.append(QNP_PX_GATE(theta_vect[iparam]), [qbit_start, qbit_start+1, qbit_start+2, qbit_start+3])
            qnp_circuit.append(QNP_OR_GATE(phi_vect[iparam]), [qbit_start, qbit_start+1, qbit_start+2, qbit_start+3])
            qbit_start+=4
            iparam+=1

    return qnp_circuit

def assign_parameters_from_file(parfile, qnp_circuit, n_layers, theta_vect, phi_vect):

    with open(parfile, 'r') as f:
        opt_params = 2.0*np.array(list(map(float, f.read().strip().split(' '))))

    n_qbits = qnp_circuit.num_qubits
    it = 0
    ip = 0
    iopt = 0
    param_values = {}

    for nl in range(2*n_layers):
        ngate = (n_qbits // 4) if nl % 2 == 0 else ((n_qbits - 1) // 4)
        qbit_start = 0  if nl % 2 == 0 else (n_qbits % 4 if n_qbits % 2 != 0 else 2)

        for ng in range(ngate):
            param_values.update({theta_vect[it]: opt_params[iopt]})
            it+=1
            iopt+=1

        for ng in range(ngate):
            param_values.update({phi_vect[ip]: opt_params[iopt]})
            ip+=1
            iopt+=1

    qnp_fix_param = qnp_circuit.assign_parameters(param_values)

    return qnp_fix_param

def initialize_HF(qnp_circuit,nelec):

    n_qbits = qnp_circuit.num_qubits
    n_space_orb = int(n_qbits/2)
    n_alpha = int(nelec/2)
    n_beta = int(nelec/2)

    for i in range(nelec):
        qnp_circuit.initialize('1', i)
   
    for i in range(nelec, n_qbits):
        qnp_circuit.initialize('0', i)
   
    return qnp_circuit

def reorder_alphabeta_to_interleaved(pauli_strings):
    reordered_pauli_strings = []

    # Check if the length of the string is even
    if len(pauli_strings[0]) % 2 != 0:
            raise ValueError(f"Pauli string '{string}' has an odd length, which is not allowed.")

    for qskstring in pauli_strings:

        # Split into two halves: first half (alpha), second half (beta)
        string = str(qskstring)
        half_len = len(string) // 2
        alpha_part = string[:half_len]
        beta_part = string[half_len:]

        # Interleave the alpha and beta parts
        interleaved = ''.join([a + b for a, b in zip(alpha_part, beta_part)])
        reordered_pauli_strings.append(interleaved)

    return reordered_pauli_strings
