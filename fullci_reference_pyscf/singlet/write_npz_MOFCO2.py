import numpy as np
from pyscf.tools import fcidump
from pyscf import ao2mo

npz_file = 'MOFCO2integrals.npz'
fcidump_file = 'reduced_FCIDUMP.MOFCO2'
Efci = -74.70598652625871
Ehf = -72.23627079645901

fcd = fcidump.read(fcidump_file)

h1e = fcd['H1']
eri = fcd['H2']
nelec = fcd['NELEC']
ecore = 0.0
n_orb = h1e.shape[0]

h2e = ao2mo.restore(1, eri, n_orb)

# -- Save integrals
np.savez(npz_file,
         Hact = h1e,
         Iact = h2e,
         Ecore = ecore,
         Ehf = Ehf,
         Efci = Efci,
         Nelec = nelec
         )

print('Complete!')
