
class InputData:
    def __init__(
            self, ashoot, dshoot, apass, dintp, ddrib, dintd, action, success):
        self.ashoot = ashoot
        self.dshoot = dshoot
        self.apass = apass
        self.dintp = dintp
        self.ddrib = ddrib
        self.dintd = dintd
        self.action = action
        self.success = success

    def discrete_input(self):
        return self
