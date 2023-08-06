import control as ct
import numpy as np


def ss_error(g, err_step=None, err_ramp=None, err_para=None):
    s = ct.TransferFunction([1, 0], [1])
    kx = None
    ess = None
    if err_step is not None:
        ess = ct.evalfr(ct.minreal(g), 0j)
        kx = 1 / err_step
    elif err_ramp is not None:
        ess = ct.evalfr(ct.minreal(s*g), 0j)
        kx = 1 / err_ramp
    elif err_para is not None:
        ess = ct.evalfr(ct.minreal(g/s), 0j)
        kx = 1 / err_para

    return kx, ess

