import control as ct
import numpy as np


def regulator(sys, poles=None, po=None, ts=None, extra_poles=[], ck=[]):
    final_poles = []

    if poles is not None:
        final_poles = poles

    if po is not None and ts is not None:
        log_po = np.log(100 / po)
        psi = log_po / np.sqrt(np.pi ** 2 + log_po ** 2)
        wn = 4 / psi / ts

        s1 = -psi * wn + 1j * wn * np.sqrt(1 - psi ** 2)
        s2 = -psi * wn - 1j * wn * np.sqrt(1 - psi ** 2)

        final_poles.append(s1)
        final_poles.append(s2)

    for p in extra_poles:
        final_poles.append(p)

    rank = np.linalg.matrix_rank(ct.ctrb(sys.A, sys.B))

    total_poles = len(final_poles)

    if total_poles < rank:
        raise BaseException(f"you have {total_poles} but you need {rank} to implement a FSFB")

    kk = ct.acker(sys.A, sys.B, final_poles)

    ak = sys.A - sys.B * kk
    bk = np.zeros((sys.A.shape[0], 1))
    default = np.zeros((1, sys.A.shape[0]))
    default[0] = 1
    ck2 = np.array(ck) if ck else default
    dk = np.array([[0]])

    return ct.ss(ak, bk, ck2, dk)

# TODO: Optimizeeeeeeeee
def regulator_with_observer(sys, poles=None, po=None, ts=None, extra_poles=[], ck=[]):
    final_poles = []

    if poles is not None:
        final_poles = poles

    if po is not None and ts is not None:
        log_po = np.log(100 / po)
        psi = log_po / np.sqrt(np.pi ** 2 + log_po ** 2)
        wn = 4 / psi / ts

        s1 = -psi * wn + 1j * wn * np.sqrt(1 - psi ** 2)
        s2 = -psi * wn - 1j * wn * np.sqrt(1 - psi ** 2)

        final_poles.append(s1)
        final_poles.append(s2)

    for p in extra_poles:
        final_poles.append(p)

    rank = np.linalg.matrix_rank(ct.ctrb(sys.A, sys.B))

    total_poles = len(final_poles)

    if total_poles < rank:
        raise BaseException(f"you have {total_poles} but you need {rank} to implement a FSFB")

    k = ct.acker(sys.A, sys.B, final_poles)

    mo = ct.obsv(sys.A, sys.C);
    obs_rank = np.linalg.matrix_rank(mo)

    print("obs_rank=", obs_rank)

    final_poles_obs = 5* final_poles

    L = ct.acker(sys.A.T, sys.C.T, final_poles_obs)
    L = L.T
    print("")
    print("L=")
    print(L)

    pa = np.concatenate([sys.A, - sys.B * k], axis=1)
    pb = np.concatenate([L * sys.C, sys.A - sys.B * k - L * sys.C], axis=1)

    alc = np.concatenate([pa, pb], axis=0)
    blc = np.concatenate([np.zeros((sys.A.shape[0], 1)), np.zeros((sys.A.shape[0], 1))])
    clc = np.concatenate([sys.C, -sys.D * k], axis=1)
    dlc = np.array([[0]])

    return ct.ss(alc, blc, clc, dlc)