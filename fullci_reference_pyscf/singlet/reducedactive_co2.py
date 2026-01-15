"""
FCI total energy: -25.762038672940832
HF total energy: -25.715752685034
FCI correlation energy: -0.04628598790683114
"""
from fcidump_utils import parse_fcidump, write_fcidump, filter_and_remap_integrals, computefci_halffilling
import numpy as np


orbital_list_occ = [7, 8]
orbital_list_NO = [9, 10]
nelec=4
norb=4
shift=142

input_fcidump = 'FCIDUMP.CO2'
output_fcidump = 'reduced_FCIDUMP.CO2'

integrals = parse_fcidump(input_fcidump)
orbital_list_tmp = orbital_list_occ+orbital_list_NO
filtered_integrals, orbital_mapping = filter_and_remap_integrals(integrals, orbital_list_tmp)
print(f"Writing {output_fcidump}")
write_fcidump(output_fcidump, filtered_integrals, orbital_mapping,nelec,norb)

fci_en, hf_energy = computefci_halffilling(output_fcidump)
print(f"\nFCI total energy: {fci_en}")
print(f"HF total energy: {hf_energy}")
print(f"FCI correlation energy: {fci_en-hf_energy}")
