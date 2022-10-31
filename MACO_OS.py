from AttackInformationTree import AttackInformationTree
import numpy as np
import random
import json


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

        find = True
        if str(discretization[0]) in self.ait.shooting:
            if str(discretization[1]) in self.ait.shooting[str(discretization[0])]:
                self.pref = self.ait.shooting[str(discretization[0])][
                    str(discretization[1])]["preference"]
                self.fail = self.ait.shooting[str(discretization[0])][
                    str(discretization[1])]["fail"]
                self.act = 0
        elif str(discretization[2]) in self.ait.passing:
            if str(discretization[3]) in self.ait.passing[str(discretization[2])]:
                self.pref = self.ait.passing[str(discretization[2])][
                    str(discretization[3])]["preference"]
                self.fail = self.ait.passing[str(discretization[2])][
                    str(discretization[3])]["fail"]
                self.act = 1
        elif str(discretization[4]) in self.ait.dribbling:
            if str(discretization[5]) in self.ait.dribbling[str(discretization[4])]:
                self.pref = self.ait.dribbling[str(discretization[4])][
                    str(discretization[5])]["preference"]
                self.fail = self.ait.dribbling[str(discretization[4])][
                    str(discretization[5])]["fail"]
                self.act = 2
        else:
            find = False
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
            # action = first[4]

            self.stats["first"][first[4]] += 1

            self.stats["second"][second[4]] += 1

        if find:
            self.stats["find"] += 1
        else:
            self.stats["not_find"] += 1

        print("Preference: ", self.pref)
        print("Best: ", self.bstpref)
        if self.pref > self.bstpref:
            self.bstpref = self.pref
            self.thefail = self.fail

        if self.bstpref < 0.001:
            self.act = 3
        return self.act

    def euclidean_distance(self, in_1, in_2):
        sum = 0.0
        for i in range(len(in_1)):
            sum += np.abs(float(in_1[i]) ** 2 - float(in_2[i]) ** 2)

        return np.sqrt(sum)


if __name__ == "__main__":
    maco = MACO_OS()
    maco.initialize(file="ait2.json")
    # print(maco.ait)
    data = []
    resps = {}
    for i in range(100000):
        data.append((1, 10, 1, 10, 1, 10))
        data.append(
            (random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10),
             random.randint(1, 10)))
    for i in data:
        act = maco.search(i)
        if act not in resps:
            resps[act] = 1
        else:
            resps[act] += 1
    print(json.dumps(maco.stats, sort_keys=True, indent=4))
    print(resps)
