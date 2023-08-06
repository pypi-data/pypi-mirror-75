import control as ct
import numpy as np
from .stady_state_error import ss_error


def lag_analytic_mode(g, wcg, pm_desired=None, psi=None, err_step=None, err_ramp=None, err_para=None):
    s = ct.TransferFunction([1, 0], [1])
    if psi is not None:
        pm_desired = 100 * psi * np.pi / 180

    if pm_desired > 2 * np.pi:
        print("remember, I need phase in radians")

    kc, ess = ss_error(g, err_step, err_ramp, err_para)

    if abs(ess) == np.inf or abs(ess) == np.nan:
        ess = None

    if ess is None or kc is None:
        assert "Inconsistent system"

    kc = kc / np.real(ess)
    print(f"kc= {kc}")

    i_point = ct.evalfr(g, 1j * wcg)

    p_mag = np.abs(i_point)
    p_angle = np.angle(i_point)

    k_mag = 1 / p_mag
    k_angle = -np.pi + pm_desired - p_angle

    alpha = k_mag * (kc * np.cos(k_angle) - k_mag) / (kc * (kc - k_mag * np.cos(k_angle)))
    tau = (k_mag * np.cos(k_angle) - kc) / (k_mag * wcg * np.sin(k_angle))

    print(f"alpha= {alpha}, tau= {tau}")

    controller = kc * (alpha * tau * s + 1) / (tau * s + 1)

    return controller
