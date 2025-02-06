class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

def runT1():
    global X
    X = X

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

