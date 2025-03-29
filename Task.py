class Task:
    def __init__(self, name, reads = None, writes = None, run = None):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run