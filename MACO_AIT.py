from AttackInformationTree import AttackInformationTree
from InputData import InputData


class MACO_AIT:
    def __init__(self):
        self.ait = AttackInformationTree()

    def populate(self, data):
        t = 0

        for i in data:
            self.ait.insert(inputData=InputData(
                ashoot=i[0],
                dshoot=i[1],
                apass=i[2],
                dintp=i[3],
                ddrib=i[4],
                dintd=i[5],
                action=i[6],
                success=i[7]
            ))
            t += 1
            if t % 1000 == 0:
                print("Processed {} rows".format(t))


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
