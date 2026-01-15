"""
FCI total energy: -55.274521861916455
HF total energy: -52.860783322647
FCI correlation energy: -2.4137385392694526
"""
from fcidump_utils import parse_fcidump, write_fcidump, filter_and_remap_integrals, computefci_halffilling
import numpy as np


orbital_list_occ = [7, 8, 9, 10, 11]
orbital_list_NO = [12, 13, 14, 15, 16]
nelec=10
norb=10
shift=142

input_fcidump = 'FCIDUMP.MOF'
output_fcidump = 'reduced_FCIDUMP.MOF'

integrals = parse_fcidump(input_fcidump)
orbital_list_tmp = orbital_list_occ+orbital_list_NO
filtered_integrals, orbital_mapping = filter_and_remap_integrals(integrals, orbital_list_tmp)
print(f"Writing {output_fcidump}")
write_fcidump(output_fcidump, filtered_integrals, orbital_mapping,nelec,norb)

fci_en, hf_energy = computefci_halffilling(output_fcidump)
print(f"\nFCI total energy: {fci_en}")
print(f"HF total energy: {hf_energy}")
print(f"FCI correlation energy: {fci_en-hf_energy}")
