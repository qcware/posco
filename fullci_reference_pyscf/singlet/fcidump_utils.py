import numpy as np
from pyscf import gto, scf, mcscf, mp, ao2mo
import pyscf
from pyscf.tools import fcidump

def parse_fcidump(filename):
    """Parse the FCIDUMP file and return a list of integrals."""
    integrals = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip header or metadata lines
            if line.startswith('&') or line.startswith('/') or '=' in line:
                continue
            if line:  # Only process lines that have actual integrals
                parts = line.split()
                value = float(parts[0])
                indices = tuple(map(int, parts[1:]))  # Convert indices to integers
                integrals.append((value, indices))
    return integrals

def filter_and_remap_integrals(integrals, orbital_list):
    """Filter integrals based on the given orbital list and remap the indices."""
    filtered_integrals = []
    
    # Create a mapping from the original orbitals to new consecutive indices
    orbital_mapping = {old: new for new, old in enumerate(sorted(orbital_list), start=1)}
    
    for value, indices in integrals:
        # Check if all non-zero indices are in the orbital list
        if all(index in orbital_mapping for index in indices if index != 0):
            # Remap the indices using the new consecutive mapping
            remapped_indices = tuple(orbital_mapping.get(index, index) for index in indices)
            filtered_integrals.append((value, remapped_indices))
    
    return filtered_integrals, orbital_mapping

def write_fcidump(filename, integrals, orbital_mapping, nelec, norb):
    """Write the filtered and remapped integrals to a new FCIDUMP file."""
    with open(filename, 'w') as f:
        # Add a basic header (you can modify this as needed)
        f.write(f"&FCI NORB={nelec}, NELEC={norb}, MS2=0, &END\n") #.format(len(orbital_mapping)))
        for value, indices in integrals:
            # Write integrals in the FCIDUMP format
            f.write(f"{value:20.12f} {' '.join(map(str, indices))}\n")

def computefci_halffilling(fcidump_file):
    """Full CI only for a half-filled active space."""

    fcd = fcidump.read(fcidump_file)
    h1 = fcd['H1']
    eri = fcd['H2']
    nelec = fcd['NELEC']
    ecore = 0.0

    mol = gto.M()
    mol.nelectron = nelec
    n_orb = h1.shape[0]
    num_alpha=int(nelec/2)
    num_beta=int(nelec/2)
    alpha_diag = [1] * num_alpha + [0] * (n_orb - num_alpha)
    beta_diag = [1] * num_beta + [0] * (n_orb - num_beta)
    eri_full = ao2mo.restore(1, eri, n_orb)

    mf = scf.RHF(mol)
    mf.get_hcore = lambda *args: np.asarray(h1)
    mf.get_ovlp = lambda *args: np.eye(h1.shape[0])
    mf.energy_nuc = lambda *args: ecore
    mf._eri = eri

    mf.init_guess = '1e'
    mf.mo_coeff = np.eye(n_orb)
    mf.mo_occ = np.array(alpha_diag) + np.array(beta_diag)
    #w, _ = np.linalg.eigh(mf.get_fock())
    #mf.mo_energy = w

    #occ_eig = mf.mo_energy[mf.mo_occ > 0]
    #sum_occ_eig = sum(occ_eig)
    #hf_energy = 2 * sum_occ_eig - mf.energy_elec()[1]

    hf_energy = (
                2 * np.einsum('ii', h1[:num_alpha, :num_alpha])
                + 2 * np.einsum('iijj', eri_full[:num_alpha, :num_alpha, :num_alpha, :num_alpha])
                - np.einsum('ijji', eri_full[:num_alpha, :num_alpha, :num_alpha, :num_alpha])
            )

    #fs = pyscf.fci.addons.fix_spin_(pyscf.fci.FCI(mf), .5)
    fs = pyscf.fci.FCI(mf)
    fs.nroots = 4

    evals = fs.kernel()[0]
    e_fci = np.min(evals)
    return e_fci, hf_energy
