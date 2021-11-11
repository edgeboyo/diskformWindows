
from datetime import date
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QDateTime, QTimer
from PyQt5.QtWidgets import QApplication, QDateTimeEdit, QDialog, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout

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
        self.clearActionLayout()
        self.part = self.disk.part[row]

        self.partitionLabel.setText(
            f"Selected partition: {self.part.shorthand()}")

        self.setUpActionLayout()

    def setUpActionLayout(self):
        actionLabel = QLabel(
            f"Selected Disk {self.disk.id} -> {self.part.shorthand()} for format")
        self.actionTime = QDateTimeEdit(QDateTime.currentDateTime())
        actionButton = QPushButton(f"Run scheduled format")
        actionButton.clicked.connect(self.checkTimeAndRun)

        self.actionLayout.addWidget(actionLabel)
        self.actionLayout.addWidget(self.actionTime)
        self.actionLayout.addWidget(actionButton)

    def checkTimeAndRun(self):
        dateTime = self.actionTime.dateTime()
        currentTime = QDateTime.currentDateTime()

        diff = currentTime.secsTo(dateTime)

        if diff < 0:
            print("Can't go back to the past")
            return

        self.diff = diff
        self.awaitScreen()

    def clearActionLayout(self):
        for i in reversed(range(self.actionLayout.count())):
            self.actionLayout.itemAt(i).widget().deleteLater()

    def disableInteractions(self):
        self.refresh.setEnabled(False)
        self.diskTable.setEnabled(False)
        self.partitionTable.setEnabled(False)

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
        self.diskTable.setEnabled(True)

        self.partitionTable.clear()
        self.partitionTable.setColumnCount(0)
        self.partitionTable.setRowCount(0)
        self.partitionTable.setEnabled(True)

        self.clearActionLayout()

    def awaitScreen(self):
        self.clearActionLayout()
        self.disableInteractions()
        formatJob = QLabel(
            f"Selected Disk {self.disk.id} -> {self.part.shorthand()} for format")
        self.timeLabel = QLabel("Remaining to format job: N/A")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advanceTime)
        self.timer.start(1000)

        timeStop = QPushButton("Stop job")
        timeStop.clicked.connect(self.stopJob)

        self.actionLayout.addWidget(formatJob)
        self.actionLayout.addWidget(self.timeLabel)
        self.actionLayout.addWidget(timeStop)

    def advanceTime(self):
        self.diff -= 1
        if self.diff <= 0:
            self.runScript()
        diff = self.diff

        secs = int(diff) % 60

        diff /= 60
        mins = int(diff) % 60

        diff /= 60
        hours = int(diff) % 60

        diff /= 24
        days = int(diff)

        remaining = "Remaining to format job: %02d:%02d:%02d:%02d" % (
            days, hours, mins, secs)

        self.timeLabel.setText(remaining)

    def stopJob(self):
        self.timer.stop()
        self.timer.deleteLater()
        self.resetGUIState()

    def runScript(self):
        self.timer.stop()
        self.timer.deleteLater()

        self.clearActionLayout()

        self.actionLayout.addWidget(QLabel("Formatting in progress..."))

        # do formatting

        # self.clearActionLayout()
        # self.build()
        # self.actionLayout.addWidget(QLabel("Formatting finished"))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
