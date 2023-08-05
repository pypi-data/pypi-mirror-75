import os
import numpy as np
import pandas as pd
import h5py


def parse_log(filename, tpye="h5"):
    with h5py.File(filename, "r") as file:
        results = {
            "controls": pd.DataFrame(np.array(file.get("controls/readout"))),
            "waveforms": pd.DataFrame(np.array(file.get("waveforms/readout"))),
            "derived_quantities": pd.DataFrame(np.array(file.get("derived_quantities/readout"))),
        }

    return results

DEFAULT_PRESSURE_RANGE = (5.0, 35.0)
DEFAULT_KEYPOINTS = [1e-8, 1.0, 1.5, 3.0]

class BreathWaveform:
    """Waveform generator with shape /‾\_"""

    def __init__(self, range=None, keypoints=None):
        self.lo, self.hi = (range or DEFAULT_PRESSURE_RANGE)
        self.xp = [0] + (keypoints or DEFAULT_KEYPOINTS)
        self.fp = [self.lo, self.hi, self.hi, self.lo, self.lo]

    @property
    def period(self):
        return self.xp[-1]

    def at(self, t):
        return np.interp(t, self.xp, self.fp, period=self.period)

    def phase(self, t):
        return np.searchsorted(self.xp, t % self.period, side="right")


class ValveCurve:
    def __init__(self, filename=None):
        filename = None or os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../../data/valve_response_bidir.csv"
        )
        df = pd.read_csv(filename, header=None)
        self.data = df.to_numpy()

    def at(self, x):
        return np.interp(np.clip(x, 0, 100) / 100, self.data[:, 0], self.data[:, 1])
