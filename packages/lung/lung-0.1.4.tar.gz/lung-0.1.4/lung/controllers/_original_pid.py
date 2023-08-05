import numpy as np

from lung.controllers.core import Controller
from lung.controllers.core import Phase
from lung.controllers._pid import PID

# Adapted directly from _PID_update in
# https://github.com/mschottdorf/Ventilator-Dev/blob/fancy_control/vent/controller/control_module.py
class OriginalPID(Controller):
    def __init__(self, K=[2.0, 2.0, 0.0], offset=0.0, RC=0.3, **kwargs):
        self.K_P, self.K_I, self.K_D = K
        self.RC = RC
        self.filters = np.zeros(3)
        self.PID = PID(waveform=self.waveform, K=K, RC=RC)

    def feed(self, state, t):
        dt = self.dt(t)
        phase = self.phase(t)
        cycle_phase = self.cycle_phase(t)

        u_in = 0
        if phase == Phase.RAMP_UP.value or phase == Phase.PIP.value:
            # __get_PID_error
            pid_signal, _ = self.PID.feed(state, cycle_phase)

            # __calculate_control_signal_in
            self.filters[0] = pid_signal
            self.filters = np.roll(self.filters, -1)
            u_in = np.mean(self.filters)

        elif phase == Phase.RAMP_DOWN.value:
            u_in = 0

        else:
            u_in = 5 * (1 - np.exp(5 * self.waveform.xp[3] - cycle_phase))

        return (u_in, self.u_out(cycle_phase))
