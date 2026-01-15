# Quantum Simulation of Carbon Capture in Periodic Metal-Organic Frameworks

This repository contains data and codes needed to reproduce the results in the paper by D. Rocca _et al._, 	arXiv:2510.02550 (2025)

For any questions, feel free to reach out to corresponding author: bkang@posco-inc.com

## Repository structure

- `Fe-MOF-74-vasp/vdWDF2`, `Fe-MOF-74-vasp/B3LYPD3`, etc.    
VASP input files required to reproduce the DFT calculations using different exchange–correlation functionals (vdW-DF2, B3LYP-D3, etc.). Each subdirectory contains inputs for structural relaxations and/or single-point calculations as well as the corresponding output files (OUTCAR).

- `Mg-MOF-74-vasp/vdWDF2`, `Mg-MOF-74-vasp/B3LYPD3`, etc.  
Analogous files for Mg-MOF-74.

- `active_space_generation_vasp`  
Input files used to generate the active spaces.
Each subdirectory is named according to the system (CO2, MOF, or MOFCO2), the kinetic energy cutoff (ENCUT), and the natural-orbital occupation threshold used to select the virtual orbitals. A `README` file with additional information is provided in this directory.

- `qnp_vqe_qiskit_simulator`  
  Each subdirectory, corresponding to the different systems (`CO2`, `MOF`, and `MOFCO2`), contains Qiskit-based Jupyter notebooks used to implement the quantum-number-preserving (QNP) ansatz for VQE.  
  The pre-optimized parameters are provided in the corresponding `optimized_params.txt` files.

- `fullci_reference_pyscf`  
Full configuration interaction reference results for different spin multiplicities, organized into three subdirectories: `singlet`, `triplet`, and `quintet`.  
  The one- and two-electron integrals used in all VQE and SQD calculations are provided in this directory.

- `sample-based_quantum_diagonalization/SQD_qiskit_simulator`  
Jupyter notebooks used to simulate sample-based quantum diagonalization (SQD) using Qiskit.

- `sample-based_quantum_diagonalization/SQD_IBM_hardware`  
Jupyter notebooks used to perform SQD on IBM quantum hardware.  
  The transpiled circuits (`.qpy` files) and the sampled bitstrings (`hwbackend_counts_reducedgates.npy`) are also provided.
