"""
FCI total energy: -55.26430256389134 
HF singlet reference: -52.860783322647
Difference: -2.40351924124434 Ha
"""
# num_alpha and num_beta are hardcoded
import numpy as np
from pyscf import gto, scf, mcscf, mp
import pyscf
from pyscf.tools import fcidump

# Load integrals from FCIDUMP file
fcidump_file = 'reduced_FCIDUMP.MOF'
fcd = fcidump.read(fcidump_file)
h1 = fcd['H1']
eri = fcd['H2']
nelec = fcd['NELEC']
n_orb = h1.shape[0]
ecore = 0.0

mol = gto.M()
mol.nelectron = nelec 
mol.norb = n_orb
num_alpha=7
num_beta=3
alpha_diag = [1] * num_alpha + [0] * (n_orb - num_alpha)
beta_diag = [1] * num_beta + [0] * (n_orb - num_beta)
print(f"spin-α occupations: alpha_diag")
print(f"spin-β occupations: beta_diag")
mol.spin=int(abs(num_alpha-num_beta))

mf = scf.ROHF(mol)
mf.nelec = (num_alpha, num_beta)
mf.get_hcore = lambda *args: np.asarray(h1)
mf.get_ovlp = lambda *args: np.eye(h1.shape[0])
mf.energy_nuc = lambda *args: ecore
mf._eri = eri  

mf.mo_coeff = np.eye(n_orb)
mf.mo_occ = np.array(alpha_diag) + np.array(beta_diag)
print(f"Orbital occupations: {np.array(alpha_diag) + np.array(beta_diag)}")
#w, _ = np.linalg.eigh(mf.get_fock())
#mf.mo_energy = w

#print("\nHF eigenvalues")
#print(w,'\n')
#print(mf.kernel())

#fs = pyscf.fci.addons.fix_spin_(pyscf.fci.FCI(mf), .5)
fs = pyscf.fci.FCI(mf)
fs.nroots = 4

evals, fci_wf = fs.kernel()
e_fci = evals[0]
print("FCI TOTAL Energy:",e_fci,'\n')

s2_expectation, multiplicity = fs.spin_square(fci_wf[0],mol.norb,mol.nelec)
print(f"Expectation value of S^2: {s2_expectation}")
print(f"Spin multiplicity: {multiplicity}")
