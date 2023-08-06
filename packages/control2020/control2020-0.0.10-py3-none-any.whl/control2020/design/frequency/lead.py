import control as ct
import numpy as np
from .stady_state_error import ss_error


def lead_compensator(g, err_step=None, err_ramp=None, err_para=None, pm_desired=None, psi=None):
    s = ct.TransferFunction([1, 0], [1])
    # all radians policy
    if psi is not None:
        pm_desired = 100*psi * np.pi/180

    if pm_desired > 2 * np.pi:
        print("remember, I need phase in radians")
    kc, ess = ss_error(g, err_step, err_ramp, err_para)

    if abs(ess) == np.inf or abs(ess) == np.nan:
        ess = None

    if ess is None or kc is None:
        assert "Inconsistent system"

    kc = kc / np.real(ess)
    print(f"kc= {kc}")

    _, pm, _, wpm = ct.margin(kc * g)
    print(pm, wpm)
    k_angle = (pm_desired - pm * np.pi / 180 + 5 * np.pi / 180)  # 5deg extra

    alpha = (1 + np.sin(k_angle)) / (1 - np.sin(k_angle))
    print(f"alpha= {alpha}")
    a = 10 * np.log10(alpha)

    print(f"A= {a}")

    mag, phase, omega = ct.bode(kc * g, Plot=False)
    arg = np.argmin(abs(20 * np.log10(mag) - -a))
    wcg = omega[arg]

    tau = 1 / np.sqrt(alpha) / wcg

    print(f"tau= {tau}")

    lead = kc * (alpha * tau * s + 1) / (tau * s + 1)
    return lead
