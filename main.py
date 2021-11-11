
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout

from diskpart import getDiskStructure, is_admin


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
        self.refresh = QPushButton("Pull disk information")
        self.refresh.clicked.connect(self.getDiskInfo)

        lists = QHBoxLayout()

        diskContainer = QVBoxLayout()

        self.diskLabel = QLabel("Selected disk: None")
        self.diskTable = QTableWidget()
        self.diskTable.cellPressed.connect(self.diskTablePress)

        diskContainer.addWidget(self.diskLabel)
        diskContainer.addWidget(self.diskTable)

        partitionContainer = QVBoxLayout()

        self.partitionLabel = QLabel("Selected partition: None")
        self.partitionTable = QTableWidget()
        self.partitionTable.cellPressed.connect(self.partTablePress)

        partitionContainer.addWidget(self.partitionLabel)
        partitionContainer.addWidget(self.partitionTable)

        lists.addLayout(diskContainer)
        lists.addLayout(partitionContainer)

        self.actionLayout = QVBoxLayout()

        mainLayout.addWidget(self.refresh)
        mainLayout.addLayout(lists)
        mainLayout.addLayout(self.actionLayout)

        self.setLayout(mainLayout)

    def getDiskInfo(self):
        self.resetGUIState()
        self.disks = getDiskStructure()

        self.diskTable.setColumnCount(1)
        self.diskTable.setRowCount(len(self.disks))
        header = self.diskTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i, disk in enumerate(self.disks):
            diskEntry = f"Disk {disk.id}"
            self.diskTable.setItem(i, 0, QTableWidgetItem(diskEntry))

    def diskTablePress(self, row, column):
        # cleaning up selected part
        self.clearActionLayout()
        self.part = None
        self.partitionLabel.setText("Selected partition: None")

        self.disk = self.disks[row]

        self.diskLabel.setText(f"Selected disk: Disk {self.disk.id}")

        self.partitionTable.clear()
        self.partitionTable.setColumnCount(1)
        self.partitionTable.setRowCount(len(self.disk.part))
        header = self.partitionTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for i, part in enumerate(self.disk.part):
            partEntry = str(part)
            self.partitionTable.setItem(i, 0, QTableWidgetItem(partEntry))

    def partTablePress(self, row, column):
        self.part = self.disk.part[row]

        self.partitionLabel.setText(
            f"Selected partition: {self.part.shorthand()}")

        self.setUpActionLayout()

    def setUpActionLayout(self):
        pass

    def clearActionLayout(self):
        for i in reversed(range(self.actionLayout.count())):
            self.actionLayout.itemAt(i).widget().deleteLater()

    def resetGUIState(self):
        self.disks = None
        self.disk = None
        self.part = None

        self.refresh.setEnabled(True)

        self.diskLabel.setText("Selected disk: None")
        self.partitionLabel.setText("Selected partition: None")

        self.diskTable.clear()
        self.diskTable.setColumnCount(0)
        self.diskTable.setRowCount(0)

        self.partitionTable.clear()
        self.partitionTable.setColumnCount(0)
        self.partitionTable.setRowCount(0)

        self.clearActionLayout()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
