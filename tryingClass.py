

class Experiment(object):

    def __init__(self, name):
        self.name = name

    class Unit(object):

        def __init__(self, mass_flow, cp, t_in, t_out):
            self.mass_flow = mass_flow
            self.cp = cp
            self.t_in = t_in
            self.t_out = t_out
            self.is_hot = Unit.is_hot

        @staticmethod
        def is_hot(cls):