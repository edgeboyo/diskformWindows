from subprocess import Popen, PIPE
import ctypes
import sys

from Disk import Disk


def getFirstInt(input):
    result = ""

    for c in input:
        if not c.isdigit():
            break
        result += c

    return int(result)


def getDiskStructure():
    script = "list disk"

    diskList = execute(script).split("\n")

    while len(diskList) > 0:
        line = diskList[0]
        del diskList[0]
        if "-" in line:
            break

    diskList = list(filter(lambda x: len(x) > 2, diskList))

    disks = []
    for disk in diskList:
        inx = disk.find("Disk")
        if inx == -1:
            raise Exception("Fatal Error: malformed stdout")
        inx += 5
        id = getFirstInt(disk[inx:])

        disks.append(Disk(id))

    for disk in disks:
        script = f"select disk {disk.id}\nlist partition"
        partList = execute(script).split("\n")

        while len(partList) > 0:
            line = partList[0]
            del partList[0]
            if "-" in line:
                break

        print(partList)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def elevate():  # dunno if I'll use this one
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit()


def execute(script=None, timeout=5):
    if script != None:
        setUpScript(script)
    command = "diskpart /s script.txt".split(" ")
    process = Popen(command, stdout=PIPE, stderr=PIPE)

    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except Exception as e:
        print(f"[Execution Error]\n{e}")
    else:
        return stdout.decode()


def setUpScript(script):
    with open('script.txt', "w") as f:
        f.write(script)


if __name__ == "__main__":
    elevate()
    getDiskStructure()
    input("...")
