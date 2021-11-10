
class Disk():
    def __init__(self, id):
        self.id = id
        self.part = []

    def addPartition(self, part):
        self.part.append(part)

    def __str__(self):
        diskRep = f"Disk {self.id}\nPartitions on disk:\n"""
        for part in self.part:
            diskRep += f"\n\t* {part}"
        return diskRep


class Partition():
    def __init__(self, id):
        self.id = id
        self.letter = None

    def assignLetter(self, letter: str):
        self.letter = letter.upper()

    def __str__(self):
        letterAssigned = "No letter assigned to partition"
        if not self.letter == None:
            letterAssigned = f"{self.letter} assigned"
        return f"Partition {self.id} -> {letterAssigned}"
