import numpy as np
from pyscf.tools import fcidump
from pyscf import ao2mo

npz_file = 'CO2integrals.npz'
fcidump_file = 'reduced_FCIDUMP.CO2'
Efci = -25.762038672940832
Ehf = -25.715752685034

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
