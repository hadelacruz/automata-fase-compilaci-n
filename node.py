#Autor: Humberto Alexander de la Cruz - 23735

class Node:
    def __init__(self, type, value=None, left=None, right=None, pos=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
        self.pos = pos
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
