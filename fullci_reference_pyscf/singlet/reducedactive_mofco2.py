""" 
FCI total energy: -74.70598652625871
HF total energy: -72.23627079645901
FCI correlation energy: -2.4697157297997023 
"""
from fcidump_utils import parse_fcidump, write_fcidump, filter_and_remap_integrals, computefci_halffilling
import numpy as np


orbital_list_occ = [4,6,9,10,11,12,13]
orbital_list_NO = [14,15,16,17,18,19,20]
nelec=14
norb=14
shift=148

input_fcidump = 'FCIDUMP.MOFCO2'
output_fcidump = 'reduced_FCIDUMP.MOFCO2'

integrals = parse_fcidump(input_fcidump)
orbital_list_tmp = orbital_list_occ+orbital_list_NO
filtered_integrals, orbital_mapping = filter_and_remap_integrals(integrals, orbital_list_tmp)
print(f"Writing {output_fcidump}")
write_fcidump(output_fcidump, filtered_integrals, orbital_mapping,nelec,norb)

fci_en, hf_energy = computefci_halffilling(output_fcidump)
print(f"\nFCI total energy: {fci_en}")
print(f"HF total energy: {hf_energy}")
print(f"FCI correlation energy: {fci_en-hf_energy}")
