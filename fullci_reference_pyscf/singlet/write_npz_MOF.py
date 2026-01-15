import numpy as np
from pyscf.tools import fcidump
from pyscf import ao2mo

npz_file = 'MOFintegrals.npz'
fcidump_file = 'reduced_FCIDUMP.MOF'
Efci = -55.274521861916455
Ehf = -52.860783322647

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
