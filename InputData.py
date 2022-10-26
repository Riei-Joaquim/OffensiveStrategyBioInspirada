from math import trunc
import numpy as np
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

    def discrete_function(self, func=None):
        T = 10 
        maxAngle = np.pi
        maxDist = 30
        dribDist = 3
        dribInt = 3

        # Shoot
        if self.ashoot >= (T - 1) * (maxAngle / T):
            self.ashoot = T
        else:
            self.ashoot = trunc(self.ashoot / (maxAngle / T) + 1)
        if self.dshoot >= (T - 1) * (maxDist / T):
            self.dshoot = T
        else:
            self.dshoot = trunc(self.dshoot / (maxDist / T) + 1)

        # Pass
        if self.apass >= (T - 1) * (maxAngle / T):
            self.apass = T
        else:
            self.apass = trunc(self.apass / (maxAngle / T) + 1)
        if self.dintp >= (T - 1) * (maxDist / T):
            self.dintp = T
        else:
            self.dintp = trunc(self.dintp / (maxDist / T) + 1)

        # Dribble
        if self.ddrib >= (T - 1) * (dribDist / T):
            self.ddrib =  T
        else:
            self.ddrib = trunc(self.ddrib / (dribDist / T) + 1)
        if self.dintd >= (T - 1) * (dribInt / T):
            self.dintd = T
        else:
            self.dintd = trunc(self.dintd / (dribInt / T) + 1)

        # Action
        if self.action == 'Shooting':
            self.action = 1
        elif self.action == 'Passing':
            self.action = 2
        elif self.action == 'Dribbling':
            self.action = 3

        print('Result')
        print(self.ashoot, self.dshoot, self.apass, self.dintp, self.ddrib, self.dintd, self.action, self.success)

if __name__ == "__main__":
    example = InputData(0.2, 14.3, 0.3,1.7, 0.7, 0.8, 'Passing', 0)
    example.discrete_function()