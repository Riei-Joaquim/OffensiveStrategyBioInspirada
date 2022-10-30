from AttackInformationTree import AttackInformationTree
from InputData import InputData


class MACO_AIT:
    def __init__(self):
        pass

    def initialize(self, size):
        self.ait = AttackInformationTree()
        self.temp = 0
        self.sg = []
        self.pheromone = [0] * size
        self.access = [0] * size
        self.heuristic = [0] * size
        self.preference = [0] * size

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

    def similarity(self, inputData):
        similarity = 0
        totalPherormone = 0

        for (it, i) in enumerate(inputData):
            for (jt, j) in enumerate(inputData):
                if i != j:
                    for k in range(0, 8):
                        similarity += pow(i[k] - j[k], 2)

                    similarity = similarity / 8
                    
                    if(similarity < 10):
                        self.sg.append(it)
                        self.sg.append(jt)

        #calculate all pheromone of similarity group
        for i in self.sg:
            totalPherormone += self.pheromone[i]
        
        #update the pherormone of similarity group with totalPherormone
        for i in self.sg:
            self.pheromone[i] += totalPherormone

    def heuristic(self, inputData):
        totalAcess = 0

        for i in self.access:
            totalAcess += i

        for (it, i) in enumerate(inputData):
            self.heuristic[it] = self.access[it] / totalAcess
    
    def preference(self, inputData, alfa, beta):
        totalPreference = 0
        for i in range (len(inputData)):
            totalPreference += pow(self.pheromone[i], alfa) * pow(self.heuristic[i], beta)

        for i in range (len(inputData)):
            self.preference[i] = (pow(self.pheromone[i], alfa) * pow(self.heuristic[i], beta)) / totalPreference

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
                self.pheromone(inputData, it)
                self.access(inputData, it)
                self.similarity(inputData, it)

            else:
                self.ait.insert(inputData)

            self.heuristic(inputData)
            
            self.preference(inputData, 2, 4)





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
