#!/usr/bin/env python

import os
from   random import randint, choice

import radical.pilot as rp

# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()

    try:
        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'local.traverse',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 64,
                   'gpus'          : 8
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)
        umgr  = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)

        cuds = list()
        for i in range(1):

            cud = rp.ComputeUnitDescription()
            cud.executable       = '%s/examples/hello_rp.sh' % os.getcwd()
            cud.arguments        = []
            cud.cpu_threads      = 1
            cud.cpu_processes    = 6
            cud.gpu_processes    = 1
            cud.gpu_process_type = rp.POSIX
            cud.cpu_process_type = rp.MPI
            cud.cpu_thread_type  = rp.POSIX
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()

    finally:
        session.close(download=False)


# ------------------------------------------------------------------------------

