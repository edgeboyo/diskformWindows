
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QTableWidget, QVBoxLayout

from diskpart import elevate, getDiskStructure, is_admin


class GUI(QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        if is_admin():
            self.build()
        else:
            self.buildNoAdmin()

    def buildNoAdmin(self):

        noAdminLayout = QVBoxLayout()
        infoLabel = QLabel(
            "You launched the app without elevated privileges...\nRerun this app as administrator")

        noAdminLayout.addWidget(infoLabel)

        self.setLayout(noAdminLayout)

    def build(self):

        mainLayout = QVBoxLayout()
        refresh = QPushButton("Pull disk information")
        refresh.clicked.connect(self.getDiskInfo)

        lists = QHBoxLayout()
        self.diskTable = QTableWidget()
        self.partitionTable = QTableWidget()

        lists.addWidget(self.diskTable)
        lists.addWidget(self.partitionTable)

        mainLayout.addWidget(refresh)
        mainLayout.addWidget(lists)

        self.setLayout(mainLayout)

    def getDiskInfo(self):
        d = getDiskStructure()
        for i in d:
            print(i)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
