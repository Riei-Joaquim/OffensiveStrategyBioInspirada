from enum import Enum

class Value:
    def __init__(self, fail, succ, sucRate, preference):
        self.fail = fail
        self.succ = succ
        self.sucRate = sucRate
        self.preference = preference

class Node:
    def __init__(self, value=None, sons=None):
        self._value = value
        self._sons = sons

class TreeType(Enum):
    SHOOTING = 0
    PASSING = 1
    DRIBBLING = 2

class AttackInfoTreeData:
    def __init__(self):
        self.Shooting = {{}}
        self.Passing =  {{}}
        self.Dribbling = {{}}

    def insert(self, type, alpha, dist, attackInfo):
        if type == AttackInfoTreeData.SHOOTING:
             self.Shooting[alpha][dist] = attackInfo
        elif type == AttackInfoTreeData.DRIBBLING:
            self.Dribbling[alpha][dist] = attackInfo
        elif type == AttackInfoTreeData.PASSING:
            self.Passing[alpha][dist] = attackInfo

    def get(self, type, alpha, dist):
        if type == AttackInfoTreeData.SHOOTING:
            return self.Shooting[alpha][dist]
        elif type == AttackInfoTreeData.DRIBBLING:
            return self.Dribbling[alpha][dist] 
        elif type == AttackInfoTreeData.PASSING:
            return self.Passing[alpha][dist]
        
        return None
