
class Disk():
    def __init__(self, id):
        self.id = id
        self.part = []

    def __str__(self):
        diskRep = f"""
Disk {self.id}

Partitions on disk:
"""[1:]
        for part in self.part:
            diskRep += f"\n\t* {part.id}"
        return diskRep


class Partition():
    def __init__(self, id):
        self.id = id
