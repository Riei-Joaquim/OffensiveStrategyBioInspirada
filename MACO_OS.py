from AttackInformationTree import AttackInformationTree
import numpy as np
import random
import json
from InputData import InputData
import numpy as np


class MACO_OS:
    def __init__(self):
        pass

    def initialize(self, file="ait.json"):
        self.ait = AttackInformationTree()
        self.ait.import_trees(file=file)
        self.pref = 0
        self.bstpref = 0
        self.fail = 0
        self.thefail = 0
        self.act = random.randint(0, 3)

        self.stats = {
            "first": {
                0: 0,
                1: 0,
                2: 0
            },
            "second": {
                0: 0,
                1: 0,
                2: 0
            },
            "find": 0,
            "not_find": 0
        }

    def search(self, discretization):
        print(discretization)
        self.pref = 0
        self.bstpref = 0
        self.fail = 0
        self.thefail = 0
        self.act = random.randint(0, 3)

        find = False
        if str(discretization[0]) in self.ait.shooting:
            if str(discretization[1]) in self.ait.shooting[str(discretization[0])]:
                self.pref = self.ait.shooting[str(discretization[0])][
                    str(discretization[1])]["preference"]
                self.fail = self.ait.shooting[str(discretization[0])][
                    str(discretization[1])]["fail"]
                self.act = 0
                print("shoot find: ", self.pref)
                find = True
        elif str(discretization[2]) in self.ait.passing:
            if str(discretization[3]) in self.ait.passing[str(discretization[2])]:
                self.pref = self.ait.passing[str(discretization[2])][
                    str(discretization[3])]["preference"]
                self.fail = self.ait.passing[str(discretization[2])][
                    str(discretization[3])]["fail"]
                self.act = 1
                print("pass find: ", self.pref)
                find = True
        elif str(discretization[4]) in self.ait.dribbling:
            if str(discretization[5]) in self.ait.dribbling[str(discretization[4])]:
                self.pref = self.ait.dribbling[str(discretization[4])][
                    str(discretization[5])]["preference"]
                self.fail = self.ait.dribbling[str(discretization[4])][
                    str(discretization[5])]["fail"]
                self.act = 2
                print("dribble find: ", self.pref)
                find = True

        if not find:
            x_1 = (discretization[0], discretization[1])
            paths = []
            for k, v in self.ait.shooting.items():
                for k2, v2 in v.items():
                    x_2 = (k, k2)
                    dist = self.euclidean_distance(x_1, x_2)
                    paths.append((dist, x_2, v2["preference"], v2["fail"], 0))

            paths.sort(key=lambda x: x[0])
            first_s = paths[0]
            second_s = paths[1]

            paths = []
            for k, v in self.ait.passing.items():
                for k2, v2 in v.items():
                    x_2 = (k, k2)
                    dist = self.euclidean_distance(x_1, x_2)
                    paths.append((dist, x_2, v2["preference"], v2["fail"], 1))

            paths.sort(key=lambda x: x[0])
            first_p = paths[0]
            second_p = paths[1]

            print()
            for i in paths:
                print(i)
            print()

            paths = []
            for k, v in self.ait.dribbling.items():
                for k2, v2 in v.items():
                    x_2 = (k, k2)
                    dist = self.euclidean_distance(x_1, x_2)
                    paths.append((dist, x_2, v2["preference"], v2["fail"], 2))

            paths.sort(key=lambda x: x[0])
            first_d = paths[0]
            second_d = paths[1]

            pref_s = (first_s[2] + second_s[2]) / 2
            fail_s = (first_s[3] + second_s[3]) / 2
            act_s = first_s[4]

            pref_p = (first_p[2] + second_p[2]) / 2
            fail_p = (first_p[3] + second_p[3]) / 2
            act_p = first_p[4]

            pref_d = (first_d[2] + second_d[2]) / 2
            fail_d = (first_d[3] + second_d[3]) / 2
            act_d = first_d[4]

            print("Distance Shoot: ", first_s[0])
            print("Distance Pass: ", first_p[0])
            print("Distance Dribble: ", first_d[0])
            print()

            print("Preference Shoot: ", pref_s)
            print("Preference Pass: ", pref_p)
            print("Preference Dribble: ", pref_d)
            print()

            if pref_s > pref_p and pref_s > pref_d:
                self.pref = pref_s
                self.fail = fail_s
                self.act = act_s
            elif pref_p > pref_s and pref_p > pref_d:
                self.pref = pref_p
                self.fail = fail_p
                self.act = act_p
            elif pref_d > pref_s and pref_d > pref_p:
                self.pref = pref_d
                self.fail = fail_d
                self.act = act_d

        if self.pref < 0.00005:
            self.act = 3
        return self.act

    def euclidean_distance(self, in_1, in_2):
        sum = 0.0
        for i in range(len(in_1)):
            sum += np.abs(float(in_1[i]) ** 2 - float(in_2[i]) ** 2)

        return np.sqrt(sum)


if __name__ == "__main__":
    maco_os = MACO_OS()
    maco_os.initialize(file="ait3.json")

    data = []

    inp = InputData(ashoot=0.418214, dshoot=9.50543, apass=0.000123,
                    dintp=0.108201, ddrib=4.811098, dintd=1.601189,
                    action=1, success=0)
    inp.discrete()
    data.append(inp.tuple[:-2])

    inp = InputData(0.378236, 20.107694, 0.000352,
                    0.38136, 4.679502, 3.384451, 0, 1)
    inp.discrete()
    data.append(inp.tuple[:-2])

    inp = InputData(0.417444, 19.14584, 0.001456,
                    1.5766, 6.279546, 4.849706, 0, 1)
    inp.discrete()
    data.append(inp.tuple[:-2])

    inp = InputData(0.547835, 16.792723, 0.000867,
                    0.938482, 6.707437, 7.082727, 0, 1)
    inp.discrete()
    data.append(inp.tuple[:-2])

    for i in data:
        act = maco_os.search(i)
        if act == 0:
            act = "Shoot"
        elif act == 1:
            act = "Pass"
        elif act == 2:
            act = "Dribble"
        else:
            act = "Back_Pass"
        print("Action: ", act)
        print()
        maco_os.initialize(file="ait3.json")
