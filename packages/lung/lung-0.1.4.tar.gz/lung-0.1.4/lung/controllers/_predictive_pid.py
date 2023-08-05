import numpy as np
from lung.controllers.core import Controller


class PredictivePID(Controller):
    def __init__(self, hallucination_length=15, **kwargs):
        # controller coeffs
        self.storage = 3
        self.errs = np.zeros(self.storage)
        self.bias_lr = 0.01
        self.bias = 0
        self.hallucination_length = hallucination_length
        self.state_buffer = np.zeros(self.storage)

    def hallucinate(self, past, steps):
        p = np.poly1d(np.polyfit(range(len(past)), past, 1))
        return np.array([p(len(past) + i) for i in range(steps)])

    def feed(self, state, t):
        dt = self.dt(t)
        cycle_phase = self.cycle_phase(t)

        self.errs[0] = self.waveform.at(t) - state
        self.errs = np.roll(self.errs, -1)
        self.bias += np.sign(np.average(self.errs)) * self.bias_lr

        # Update State
        self.state_buffer[0] = state
        self.state_buffer = np.roll(self.state_buffer, -1)

        hallucinated_states = self.hallucinate(self.state_buffer, self.hallucination_length)
        hallucinated_errors = [
            self.waveform.at(t + (j + 1) * dt) - hallucinated_states[j]
            for j in range(self.hallucination_length)
        ]

        if cycle_phase < 0.1:
            u = np.sum(self.errs) + self.bias
        else:
            new_av = (np.sum(self.errs) + np.sum(hallucinated_errors)) * (
                self.storage / (self.storage + len(hallucinated_errors))
            )
            u = new_av + self.bias
        return (u, self.u_out(cycle_phase))
