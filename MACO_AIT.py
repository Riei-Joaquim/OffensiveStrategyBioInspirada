from AttackInformationTree import AttackInformationTree
from InputData import InputData


class MACO_AIT:
    def __init__(self):
        pass

    def initialize(self, size):
        self.ait = AttackInformationTree()
        self.temp = 0
        self.pheromone = [0] * size
        self.access = [0] * size
        self.heuristic = [0] * size

    def populate(self, data):
        for it, i in enumerate(data):
            inputData = InputData(i[0], i[1], i[2], i[3], i[4], i[5])

            #shoot
            if inputData.action == 0:
                if inputData.ashoot in self.ait.shooting:
                    if inputData.dshoot in self.ait.shooting:
                        find = True
                    else:
                        find = False
                else:
                    find = False
            #pass
            elif inputData.action == 1:
                if inputData.apass in self.ait.passing:
                    if inputData.dintp in self.ait.passing:
                        find = True
                    else:
                        find = False
                else:
                    find = False
            #dribble
            elif inputData.action == 2:
                if inputData.ddrib in self.ait.dribbling:
                    if inputData.dintd in self.ait.dribbling:
                        find = True
                    else:
                        find = False
                else:
                    find = False

            #find the state on the tree
            if find:
                pass
            else:
                self.ait.insert(inputData)

    def pheromone(self, inputData, index):
        evaporationCoefficient = 0.1
        deltaTau = 1

        if(inputData.success):
            self.pheromone[index] = (1 - evaporationCoefficient) * self.pheromone[index] + deltaTau * 3
        else:
            self.pheromone[index] = (1 - evaporationCoefficient) * self.pheromone[index] + deltaTau * 0
    
    def access(self, inputData, index):
        if(inputData.success):
            self.access[index] += 1
        else:
            self.access[index] += 0

    def similarity(self, inputData, index):
        pass


if __name__ == "__main__":
    data = []
    data.append([0, 0, 0, 0, 0, 0, 0, 0])
    data.append([0, 0, 0, 0, 0, 0, 0, 1])
    data.append([1, 0, 0, 0, 0, 0, 0, 0])
    data.append([1, 0, 0, 0, 0, 0, 0, 1])
    data.append([1, 2, 0, 0, 0, 0, 0, 1])
    data.append([0, 0, 0, 0, 0, 0, 1, 1])
    data.append([0, 0, 0, 0, 0, 0, 2, 0])
    maco = MACO_AIT()
    maco.populate(data)
    print(maco.ait)
