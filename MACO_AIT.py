from AttackInformationTree import AttackInformationTree
from InputData import InputData
import pandas as pd
import numpy as np
import time


class MACO_AIT:
    def __init__(self):
        pass

    def _initialize(self, size):
        self.ait = AttackInformationTree()
        self.temp = 0
        self.sg = [[] for i in range(size)]
        self.pheromone = [0 for i in range(size)]
        self.access = [0 for i in range(size)]
        self.heuristic = [0 for i in range(size)]
        self.preference = [0 for i in range(size)]
        self.hash = {}

    def _pheromone(self, inputData, index):
        evaporationCoefficient = 0.1
        deltaTau = 1

        if (inputData.success):
            self.pheromone[index] = (
                1 - evaporationCoefficient) * self.pheromone[index] + deltaTau * 3
        else:
            self.pheromone[index] = (
                1 - evaporationCoefficient) * self.pheromone[index] + deltaTau * 0

    def _access(self, inputData, index):
        if (inputData.success):
            self.access[index] += 1
        else:
            self.access[index] += 0

    def _similarity(self, inputData, index):
        similarity = 0

        data = []
        groups = []
        groups_keys = self.hash.keys()

        for i in self.hash:
            data.append(self.hash[i][0])
            groups.append((self.hash[i][0], self.hash[i][1]))

        for j, jt in groups:
            for (it, i) in enumerate(data):
                similarity = 0
                if j.tuple != i.tuple:
                    for k in range(0, 6):
                        similarity += pow(j.tuple[k] - i.tuple[k], 2)

                    similarity = similarity / 6
                    if (similarity < 2):
                        if it not in self.sg[jt]:
                            self.sg[jt].append(it)

        for j in self.sg:
            for i in j:
                # update the pherormone of similarity group with totalPherormone
                if inputData.success:
                    self.pheromone[i] += 3

    def _heuristic(self, data):
        totalAcess = 0

        for i in self.access:
            totalAcess += i

        for (it, i) in enumerate(data):
            self.heuristic[it] = self.access[it] / totalAcess

    def _preference(self, data, alfa, beta):
        totalPreference = 0
        for i in range(len(data)):
            totalPreference += pow(self.pheromone[i],
                                   alfa) * pow(self.heuristic[i], beta)

        for i in range(len(data)):
            self.preference[i] = (
                pow(self.pheromone[i],
                    alfa) * pow(self.heuristic[i],
                                beta)) / totalPreference

    def _populate(self, data):
        print("Initialize")
        self._initialize(len(data))
        for it, i in enumerate(data):
            inputData = i
            print(inputData)
            # shoot
            if inputData.action == 0:
                if inputData.ashoot in self.ait.shooting:
                    if inputData.dshoot in self.ait.shooting[inputData.ashoot]:
                        find = True
                    else:
                        find = False
                else:
                    find = False
            # pass
            elif inputData.action == 1:
                if inputData.apass in self.ait.passing:
                    if inputData.dintp in self.ait.passing[inputData.apass]:
                        find = True
                    else:
                        find = False
                else:
                    find = False
            # dribble
            elif inputData.action == 2:
                if inputData.ddrib in self.ait.dribbling:
                    if inputData.dintd in self.ait.dribbling[inputData.ddrib]:
                        find = True
                    else:
                        find = False
                else:
                    find = False

            # find the state on the tree
            if find:
                print("Find")
                print("Action: ", inputData.action)
                print("Result: ", inputData.success)

                self._pheromone(inputData, it)
                hash_it = it
                if inputData.action == 0:
                    hash_it = self.hash[(
                        inputData.ashoot, inputData.dshoot)][1]
                    self._access(inputData, hash_it)
                elif inputData.action == 1:
                    hash_it = self.hash[(inputData.apass, inputData.dintp)][1]
                    self._access(inputData, hash_it)
                elif inputData.action == 2:
                    hash_it = self.hash[(inputData.ddrib, inputData.dintd)][1]
                    self._access(inputData, hash_it)

                self._similarity(inputData, hash_it)

            else:
                print("Not Find")
                print("Insert on the tree")
                self.ait.insert(inputData)

                print("Action: ", inputData.action)
                print("Result: ", inputData.success)

                self._pheromone(inputData, it)

                self._access(inputData, it)

                if inputData.action == 0:
                    self.hash[(inputData.ashoot, inputData.dshoot)] = (
                        inputData, it)
                elif inputData.action == 1:
                    self.hash[(inputData.apass, inputData.dintp)] = (
                        inputData, it)
                elif inputData.action == 2:
                    self.hash[(inputData.ddrib, inputData.dintd)] = (
                        inputData, it)

            print("Pheromone Level: ", self.pheromone)
            print("Access Values: ", self.access)
            print("Similarity: ", self.sg)
            print("----------------------------------------------")

        self._heuristic(data)
        print("Heuristic: ", self.heuristic)

        self._preference(data, 2, 4)
        print("Preference: ", self.preference)

        groups = []
        for i in self.hash:
            groups.append((i, self.hash[i][0], self.hash[i][1]))

        for path, inputData, hash_it in groups:
            self.ait.update_leaf(
                inputData, self.pheromone[hash_it],
                self.preference[hash_it])

    def _export_trees(self, file="ait.json"):
        self.ait.export_trees(file=file)


if __name__ == "__main__":
    data = []

    df = pd.read_csv('test.csv')

    for i in range(len(df)):
        if df.iloc[i]["action"] == "s":
            action = 0
        elif df.iloc[i]["action"] == "p":
            action = 1
        elif df.iloc[i]["action"] == "d":
            action = 2

        if df.iloc[i]["result"] == "sucess":
            result = 1
        else:
            result = 0

        for column in df.columns:
            if df.iloc[i][column] == "nan":
                continue

        inputData = InputData(df.iloc[i]["gap_angle"],
                              df.iloc[i]["shooting_distance"],
                              df.iloc[i]["passing_angle"],
                              df.iloc[i]["intercept_distance"],
                              df.iloc[i]["dribbling_distance"],
                              df.iloc[i]["defender_intercept_distance"],
                              action,
                              result)
        inputData.discrete()
        data.append(inputData)

    maco = MACO_AIT()
    maco._populate(data)
    print(maco.ait)
    # for i in maco.hash.keys():
    #     print(i)
    #     print(maco.hash[i][0].tuple)
    print(len(maco.hash))
    maco._export_trees()
