Input Files and Workflow

The sudirectories contain the VASP input files used in the active space calculations, listed below in the sequential order of the computational workflow.

1. `INCAR.HF` performs the Hartree–Fock (HF) calculation.

2. `INCAR.HF.diag` performs a non-self-consistent diagonalization of the Hamiltonian.
Optional but can be useful for comparison purposes (i.e. HF vs. active space orbital energies).

3. `INCAR.wan` performe the Wannierization of the occupied states.
This step produces a wavefunction file WAVECAR.wan, which must overwrite the original `WAVECAR`: `cp WAVECAR.wan WAVECAR`.
 
4. `INCAR.srt` moves the orbitals localized on the fragment of interest to the highest band indices in the `WAVECAR` file; the fragment is defined by selecting the atoms of interest (e.g. `EMBED_SITES = 34 35 41 42 53`).
After this step, it is necessary to copy the produced wavefunction file:
`cp WAVECAR.srt WAVECAR`

5. `INCAR.parden`
computes partial charges for visualization.
Not strictly required, but useful to verify that the localization procedure worked correctly.

6. `INCAR.HF.diag.recan` recanonicalizes the orbitals localized on the fragment.

7. `INCAR.parden.recan`
computes partial charges for visualization after recanonicalization.
Optional but useful for validation.

8. `INCAR.mp2no.recan`
computes MP2 natural orbitals, including only the active subset of localized occupied orbitals.
All remaining orbitals are frozen using the `NFREEZE` flag.
At the end of this step, copy:
`cp WAVECAR.FNO WAVECAR`.

9. `INCAR.recan.nos`
recanonicalizes the natural orbitals.
The range of orbitals to be recanonicalized is determined by `NBANDSLOW` and `NBANDSHIGH`.

10. `INCAR.parden.nosrecan`
computes partial charges for visualization after natural-orbital recanonicalization.
Optional.

11. `INCAR.mp2`
computes MP2 energies considering only the selected fragment and the selected natural orbitals.

12. `INCAR.fci`
writes one- and two-electron integrals to an `FCIDUMP` file.
Due to the potentially large size of `FCIDUMP` files, this step was not performed in all cases.
