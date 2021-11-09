from subprocess import Popen, PIPE
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def elevate():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        exit()


def setUpScript():
    script = """
LIST DISK
"""[1:]
    with open('script.txt', "w") as f:
        f.write(script)


if __name__ == "__main__":
    elevate()

    print('Elevated!')

    setUpScript()

    command = "diskpart /s script.txt".split(" ")
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    try:
        stdout, stderr = process.communicate('\0', timeout=5)
    except Exception as e:
        print(e)
    finally:
        print(stdout)

    input("Press ENTER to return...")
