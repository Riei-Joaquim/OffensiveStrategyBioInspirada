from AttackInformationTree import AttackInformationTree
import numpy as np
import random


class MACO_OS:
    def __init__(self):
        pass

    def initialize(self):
        self.ait = AttackInformationTree()
        self.ait.import_trees(file="ait.json")
        self.pref = 0
        self.bstpref = 0
        self.fail = 0
        self.thefail = 0
        self.act = 0

    def search(self, discretization):
        if discretization[0] in self.ait.shooting:
            if discretization[1] in self.ait.shooting[discretization[0]]:
                self.pref = self.ait.shooting[discretization[0]][
                    discretization[1]]["preference"]
                self.fail = self.ait.shooting[discretization[0]][
                    discretization[1]]["fail"]
                action = 0
        elif discretization[2] in self.ait.passing:
            if discretization[3] in self.ait.passing[discretization[2]]:
                self.pref = self.ait.passing[discretization[2]][
                    discretization[3]]["preference"]
                self.fail = self.ait.passing[discretization[2]][
                    discretization[3]]["fail"]
                action = 1
        elif discretization[4] in self.ait.dribbling:
            if discretization[5] in self.ait.dribbling[discretization[4]]:
                self.pref = self.ait.dribbling[discretization[4]][
                    discretization[5]]["preference"]
                self.fail = self.ait.dribbling[discretization[4]][
                    discretization[5]]["fail"]
                action = 2
        else:
            x_1 = (discretization[0], discretization[1])
            paths = []
            for k, v in self.ait.shooting.items():
                for k2, v2 in v.items():
                    x_2 = (k, k2)
                    dist = self.euclidean_distance(x_1, x_2)
                    paths.append((dist, x_2, v2["preference"], v2["fail"], 0))

            for k, v in self.ait.passing.items():
                for k2, v2 in v.items():
                    x_2 = (k, k2)
                    dist = self.euclidean_distance(x_1, x_2)
                    paths.append((dist, x_2, v2["preference"], v2["fail"], 1))

            for k, v in self.ait.dribbling.items():
                for k2, v2 in v.items():
                    x_2 = (k, k2)
                    dist = self.euclidean_distance(x_1, x_2)
                    paths.append((dist, x_2, v2["preference"], v2["fail"], 2))

            paths.sort(key=lambda x: x[0])
            first = paths[0]
            second = paths[1]

            self.pref = (first[2] + second[2]) / 2
            self.fail = (first[3] + second[3]) / 2
            action = first[4]

        if self.pref > self.bstpref:
            self.bstpref = self.pref
            self.thefail = self.fail
            self.act = action

        if self.bstpref < 0.25:
            self.act = 3

        return self.act

    def euclidean_distance(self, in_1, in_2):
        sum = 0.0
        for i in range(len(in_1)):
            sum += float(in_1[i]) ** 2 - float(in_2[i]) ** 2

        return np.sqrt(sum)


if __name__ == "__main__":
    maco = MACO_OS()
    maco.initialize()
    discretizate = [2, 4, 2, 2, 3, 4]
    data = []
    data.append([2, 4, 2, 2, 3, 4])
    data.append([2, 4, 2, 2, 3, 4])
    data.append([2, 4, 2, 2, 3, 4])
    data.append([2, 4, 2, 2, 3, 4])
    data.append([2, 4, 2, 2, 3, 4])
    data.append([2, 4, 2, 2, 3, 4])
    data.append([2, 4, 2, 2, 3, 4])
    for i in data:
        act = maco.search(i)
        print(act)
