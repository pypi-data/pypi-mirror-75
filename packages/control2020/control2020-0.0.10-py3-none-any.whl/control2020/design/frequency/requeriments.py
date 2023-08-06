import control as ct
import numpy as np


def frequency_requirements(g, gain_margin=None, phase_margin=None):
    gains = []

    gm, pm, _, _ = ct.margin(g)
    if gain_margin is not None:
        gains.append(10 ** (-(gain_margin - gm) / 20))

    if phase_margin is not None:
        mag, phase, omega = ct.bode(g, Plot=False)
        arg = np.argmin(abs(phase - (phase_margin - np.pi)))
        m = 20 * np.log10(mag[arg])
        gains.append(10 ** (-m / 20))

    return np.prod(gains)