import numpy as np
from lung.controllers.core import Controller
from lung.controllers.core import LinearForecaster
from lung.controllers._pid import PID
from lung.controllers._lookahead import Lookahead


class PredictiveBiasPI(Controller):
    def __init__(self, p=0.5, i=2.5, RC=0.06, lookahead_steps=15, bias_lr=0.01, **kwargs):
        # controller coeffs
        self.bias_lr = bias_lr
        self.bias = 0
        self.storage = 3
        self.forecaster = LinearForecaster(self.storage)
        self.pid = PID(K=[p, i, 0.0], RC=RC, waveform=self.waveform)
        self.base_controller = Lookahead(self.forecaster, self.pid, lookahead_steps)

    def feed(self, state, t):
        err = self.waveform.at(t) - state
        cycle_phase = self.cycle_phase(t)

        self.bias = self.bias + np.sign(err) * self.bias_lr
        base_control, _ = self.base_controller.feed(state, cycle_phase)
        return (base_control + self.bias, self.u_out(cycle_phase))
