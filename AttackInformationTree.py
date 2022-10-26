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
        inputDataDiscrete = inputData.discrete_input()
        if inputDataDiscrete.action == 0:
            if inputDataDiscrete.ashoot not in self.shooting:
                self.shooting[inputDataDiscrete.ashoot] = {}
            if inputDataDiscrete.dshoot not in self.shooting[inputDataDiscrete.ashoot]:
                self.shooting[inputDataDiscrete.ashoot][inputDataDiscrete.dshoot] = {
                    "fail": 0, "succ": 0, "sucRate": 0.0, "preference": 0.0}
            if inputDataDiscrete.success:
                self.shooting[inputDataDiscrete.ashoot][inputDataDiscrete.dshoot]["succ"] += 1
            else:
                self.shooting[inputDataDiscrete.ashoot][inputDataDiscrete.dshoot]["fail"] += 1
        elif inputDataDiscrete.action == 1:
            if inputDataDiscrete.apass not in self.passing:
                self.passing[inputDataDiscrete.apass] = {}
            if inputDataDiscrete.dintp not in self.passing[inputDataDiscrete.apass]:
                self.passing[inputDataDiscrete.apass][inputDataDiscrete.dintp] = {
                    "fail": 0, "succ": 0, "sucRate": 0.0, "preference": 0.0}
            if inputDataDiscrete.success:
                self.passing[inputDataDiscrete.apass][inputDataDiscrete.dintp]["succ"] += 1
            else:
                self.passing[inputDataDiscrete.apass][inputDataDiscrete.dintp]["fail"] += 1
        elif inputDataDiscrete.action == 2:
            if inputDataDiscrete.ddrib not in self.dribbling:
                self.dribbling[inputDataDiscrete.ddrib] = {}
            if inputDataDiscrete.dintd not in self.dribbling[inputDataDiscrete.ddrib]:
                self.dribbling[inputDataDiscrete.ddrib][inputDataDiscrete.dintd] = {
                    "fail": 0, "succ": 0, "sucRate": 0.0, "preference": 0.0}
            if inputDataDiscrete.success:
                self.dribbling[inputDataDiscrete.ddrib][inputDataDiscrete.dintd]["succ"] += 1
            else:
                self.dribbling[inputDataDiscrete.ddrib][inputDataDiscrete.dintd]["fail"] += 1

    def __str__(self):
        return str("Shooting: " + json.dumps(self.shooting, sort_keys=True, indent=4)) + \
            str("\n\nPassing: " + json.dumps(self.passing, sort_keys=True, indent=4)) + \
            str("\n\nDribbling: " + json.dumps(self.dribbling, sort_keys=True, indent=4))
