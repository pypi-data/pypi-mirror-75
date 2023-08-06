import control as ct
import numpy as np
from .stady_state_error import ss_error


def pid_by_frequency(g, po, ts, err_step=None, err_ramp=None, err_para=None):
    s = ct.TransferFunction([1, 0], [1])
    ki, ess = ss_error(g/s, err_step, err_ramp, err_para)

    if abs(ess) == np.inf or abs(ess) == np.nan:
        ess = None

    if ess is None or ki is None:
        assert "Inconsistent system"

    ki = ki / np.real(ess)
    print("ki=", ki)
    log_po = np.log(100 / po)
    psi = log_po / np.sqrt(np.pi ** 2 + log_po ** 2)

    wn = 4 / psi / ts
    print("wn=", wn, "psi=", psi)

    pm = 100 * psi
    wcp = wn

    p_cut = ct.evalfr(g, wcp * 1j)
    p_cut_mag = np.abs(p_cut)
    p_cut_angle = np.angle(p_cut)

    controller_mag = 1 / p_cut_mag
    controller_angle = -np.pi + pm * np.pi / 180 - p_cut_angle

    kp = controller_mag * np.cos(controller_angle)
    kd = (controller_mag * np.sin(controller_angle) + ki / wcp) / wcp

    print(f"pm= {pm}, ki= {ki}, kp= {kp}, kd= {kd}")
    controller = kp + kd * s + ki / s

    return controller
