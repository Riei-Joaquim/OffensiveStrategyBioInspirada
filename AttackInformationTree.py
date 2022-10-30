from enum import Enum
from InputData import InputData
import json


class TreeType(Enum):
    SHOOTING = 0
    PASSING = 1
    DRIBBLING = 2


class AttackInformationTree:
    def __init__(self):
        self.shooting = {}
        self.passing = {}
        self.dribbling = {}

    def insert(self, inputData: InputData):
        inputDataCopy = inputData
        if inputDataCopy.action == 0:
            if inputDataCopy.ashoot not in self.shooting:
                self.shooting[inputDataCopy.ashoot] = {}
            if inputDataCopy.dshoot not in self.shooting[inputDataCopy.ashoot]:
                self.shooting[inputDataCopy.ashoot][inputDataCopy.dshoot] = {
                    "fail": 0, "succ": 0, "sucRate": 0, "preference": 0}
        elif inputDataCopy.action == 1:
            if inputDataCopy.apass not in self.passing:
                self.passing[inputDataCopy.apass] = {}
            if inputDataCopy.dintp not in self.passing[inputDataCopy.apass]:
                self.passing[inputDataCopy.apass][inputDataCopy.dintp] = {
                    "fail": 0, "succ": 0, "sucRate": 0, "preference": 0}
        elif inputDataCopy.action == 2:
            if inputDataCopy.ddrib not in self.dribbling:
                self.dribbling[inputDataCopy.ddrib] = {}
            if inputDataCopy.dintd not in self.dribbling[inputDataCopy.ddrib]:
                self.dribbling[inputDataCopy.ddrib][inputDataCopy.dintd] = {
                    "fail": 0, "succ": 0, "sucRate": 0, "preference": 0}

    def update_leaf(self, inputData, succ_rate, pref):
        inputDataCopy = inputData
        if inputDataCopy.action == 0:
            self.shooting[inputDataCopy.ashoot][inputDataCopy.dshoot][
                "sucRate"] = succ_rate
            self.shooting[inputDataCopy.ashoot][inputDataCopy.dshoot][
                "preference"] = pref
            if inputDataCopy.success:
                self.shooting[inputDataCopy.ashoot][inputDataCopy.dshoot][
                    "succ"] += 1
            else:
                self.shooting[inputDataCopy.ashoot][inputDataCopy.dshoot][
                    "fail"] += 1
        elif inputDataCopy.action == 1:
            self.passing[inputDataCopy.apass][inputDataCopy.dintp][
                "sucRate"] = succ_rate
            self.passing[inputDataCopy.apass][inputDataCopy.dintp][
                "preference"] = pref
            if inputDataCopy.success:
                self.passing[inputDataCopy.apass][inputDataCopy.dintp][
                    "succ"] += 1
            else:
                self.passing[inputDataCopy.apass][inputDataCopy.dintp][
                    "fail"] += 1
        elif inputDataCopy.action == 2:
            self.dribbling[inputDataCopy.ddrib][inputDataCopy.dintd][
                "sucRate"] = succ_rate
            self.dribbling[inputDataCopy.ddrib][inputDataCopy.dintd][
                "preference"] = pref

            if inputDataCopy.success:
                self.dribbling[inputDataCopy.ddrib][inputDataCopy.dintd][
                    "succ"] += 1
            else:
                self.dribbling[inputDataCopy.ddrib][inputDataCopy.dintd][
                    "fail"] += 1

    def __str__(self):
        return str("Shooting: " + json.dumps(self.shooting, sort_keys=True, indent=4)) + \
            str("\n\nPassing: " + json.dumps(self.passing, sort_keys=True, indent=4)) + \
            str("\n\nDribbling: " + json.dumps(self.dribbling, sort_keys=True, indent=4))

    def export_trees(self, file=None):
        big_tree = {
            "shooting": self.shooting,
            "passing": self.passing,
            "dribbling": self.dribbling
        }

        with open('ait.json' if file is None else file, 'w') as outfile:
            json.dump(big_tree, outfile)

    def import_trees(self, file=None):
        with open('ait.json' if file is None else file) as json_file:
            big_tree = json.load(json_file)
            self.shooting = big_tree["shooting"]
            self.passing = big_tree["passing"]
            self.dribbling = big_tree["dribbling"]
