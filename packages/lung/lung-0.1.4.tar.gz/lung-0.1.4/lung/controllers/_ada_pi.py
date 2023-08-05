import numpy as np
from lung.controllers.core import Controller
from lung.controllers.core import LinearForecaster
from lung.controllers._pid import PID
from lung.controllers.core import Phase
from lung.controllers._lookahead import Lookahead


class AdaPI(Controller):
    def __init__(
        self, p=0.5, i=1.0, RC=0.06, lookahead_steps=15, bias_lr=0.01, c_lr=0.001, **kwargs
    ):
        # controller coeffs
        self.bias_lr = bias_lr
        self.bias = 0
        self.c_lr = c_lr
        self.c = 1.0
        self.storage = 3
        self.overshoot_penalty = 5
        self.forecaster = LinearForecaster(self.storage)
        self.pid = PID(K=[p, i, 0.0], RC=RC, waveform=self.waveform)
        self.base_controller = Lookahead(self.forecaster, self.pid, lookahead_steps)

    def feed(self, state, t):

        err = self.waveform.at(t) - state
        phase = self.phase(t)
        cycle_phase = self.cycle_phase(t)

        if phase == Phase.RAMP_UP.value:
            base_control, _ = self.base_controller.feed(state, t)
            adj_base_control = self.c * base_control
            self.u = adj_base_control + self.bias
        elif phase == Phase.PIP.value:
            self.bias = self.bias + err * self.bias_lr * (1 + (err < -1) * self.overshoot_penalty)
            self.c = self.c + err * self.c_lr * (1 + (err < -1) * self.overshoot_penalty)
            base_control, _ = self.base_controller.feed(state, t)
            adj_base_control = self.c * base_control
            self.u = adj_base_control + self.bias
        elif phase == Phase.RAMP_DOWN.value:
            u_in = 0
        else:
            u_in = 5 * (1 - np.exp(5 * self.waveform.xp[3] - cycle_phase))

        return (self.u, self.u_out(cycle_phase))
