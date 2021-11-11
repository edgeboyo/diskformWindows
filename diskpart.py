from subprocess import Popen, PIPE
import ctypes
import sys

from Disk import Disk, Partition


def getFirstInt(input):
    result = ""

    for c in input:
        if not c.isdigit():
            break
        result += c

    return int(result)


def clearToTableContent(entryList, parter="-"):
    while len(entryList) > 0:
        line = entryList[0]
        del entryList[0]
        if parter in line:
            break

    if entryList == []:
        return None

    return list(filter(lambda x: len(x) != 0, entryList))


def getDiskStructure():
    script = "list disk"

    diskList = execute(script).split("\n")

    disks: list[Disk] = []
    for disk in clearToTableContent(diskList):
        inx = disk.find("Disk")
        if inx == -1:
            raise Exception("Fatal Error: malformed stdout")
        inx += 5
        id = getFirstInt(disk[inx:])

        disks.append(Disk(id))

    for disk in disks:
        script = f"select disk {disk.id}\nlist partition"
        partList = execute(script).split("\n")

        for part in clearToTableContent(partList):
            inx = part.find("Partition")
            if inx == -1:
                raise
            inx += 10
            id = getFirstInt(part[inx:])

            disk.addPartition(Partition(id))

            script = f"select disk {disk.id}\nselect partition {id}\ndetail partition"

            letter = execute(script).split('\n')

            letter = clearToTableContent(letter, "---")

            if letter != None and len(letter) == 1:
                [letter] = letter
                inx = letter.find('Volume')
                inx += 7

                for c in letter[inx:][:10]:  # arbitrary limit set
                    if c.isalpha():
                        disk.part[-1].assignLetter(c)
                        break

    return disks


def performFormat(diskId, paritionId):
    # can add a dialog to select later
    script = f"select disk {diskId}\nselect partition {paritionId}\nformat fs=ntfs quick"

    return execute(script, 60 * 60 * 60)


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


if __name__ == "__main__":  # for testing
    elevate()
    getDiskStructure()
    input("...")
