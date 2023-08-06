import control as ct
import numpy as np
from .stady_state_error import ss_error


def lag_compensator(g, err_step=None, err_ramp=None, err_para=None, pm_desired=None, psi=None):
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

    print("kc=", kc)

    phi = (pm_desired + 7 * np.pi / 180) - np.pi

    print("phi=", phi)

    mag, phase, omega = ct.bode(kc * g, Plot=False)
    arg = np.argmin(abs(phase - phi))

    wcg = omega[arg]
    print(f"wcg= {wcg}")

    gain = 20 * np.log10(mag[arg])
    a = 0 - gain
    print(f"A= {a}")

    alpha = 10 ** (a / 20)
    tau = 10 / alpha / wcg

    lag = kc * (alpha * tau * s + 1) / (tau * s + 1)

    return lag
