from lung.controllers.core import Controller


# generic PID controller
class PID(Controller):
    def __init__(self, K=[3, 4, 0], RC=0.5, **kwargs):
        # controller coeffs
        self.K_P, self.K_I, self.K_D = K

        # controller states
        self.P, self.I, self.D = 0, 0, 0

        self.RC = RC

    def feed(self, state, t):
        err = self.waveform.at(t) - state

        dt = self.dt(t)

        self.decay = dt / (dt + self.RC)

        self.I += self.decay * (err - self.I)
        self.D += self.decay * (err - self.P - self.D)
        self.P = err

        u_in = self.K_P * self.P + self.K_I * self.I + self.K_D * self.D

        return (u_in, self.u_out(t))
