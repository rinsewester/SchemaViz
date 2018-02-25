#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mainwindow of SDFkit showing all widgets.

author: Rinse Wester

"""

import sys
from PyQt5.QtWidgets import QDockWidget, QListWidget, QHBoxLayout, QWidget, QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, qApp
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QIcon, QDrag

from schemaview import SchemaView, SchemaScene
import schemastyle

class CompListWidget(QListWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(128)
        self.setDragEnabled(True)

    def mousePressEvent(self, event):
        curItem = self.itemAt(event.pos())
        if curItem is not None:
            mimedata = QMimeData()
            mimedata.setText(curItem.text())
            drag = QDrag(self)
            drag.setMimeData(mimedata)
            drag.exec(Qt.MoveAction)

class MainWindow(QMainWindow):

    DEFAULT_FILE = 'schemas/schem1.json'

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        openAction = QAction(QIcon('images/open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open schematic')
        openAction.triggered.connect(self.openFile)

        saveAction = QAction(QIcon('images/save.png'), '&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save schematic')
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QAction(QIcon('images/save.png'), 'Save &as', self)
        saveAsAction.setShortcut('Ctrl+Shift+S')
        saveAsAction.setStatusTip('Save schematic as')
        saveAsAction.triggered.connect(self.saveFileAs)

        exitAction = QAction(QIcon('images/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        graphmenu = self.menuBar().addMenu('&Schema')
        graphmenu.addAction(openAction)
        graphmenu.addAction(saveAction)
        graphmenu.addAction(saveAsAction)
        graphmenu.addAction(exitAction)

        resetZoomAction = QAction('&Reset zoom', self)
        resetZoomAction.setShortcut('Ctrl+0')
        resetZoomAction.setStatusTip('Reset zoom')

        zoomInAction = QAction('Zoom &in', self)
        zoomInAction.setShortcut('Ctrl+=')
        zoomInAction.setStatusTip('Zoom in')

        zoomOutAction = QAction('&Zoom out', self)
        zoomOutAction.setShortcut('Ctrl+-')
        zoomOutAction.setStatusTip('Zoom out')

        viewmenu = self.menuBar().addMenu('&View')
        viewmenu.addAction(zoomInAction)
        viewmenu.addAction(zoomOutAction)
        viewmenu.addAction(resetZoomAction)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)

        # Use mac unitfied toolbar when running on mac
        if sys.platform == 'darwin':
            self.setUnifiedTitleAndToolBarOnMac(True)

        self.currentFile = MainWindow.DEFAULT_FILE

        self.schemaview = SchemaView()
        self.schemascene = SchemaScene()
        self.schemascene.loadFromFile(self.currentFile)
        self.schemaview.setScene(self.schemascene)
        self.schemaview.resetView()

        # connect the view menu actions to the graphwidget
        zoomInAction.triggered.connect(self.schemaview.zoomIn)
        zoomOutAction.triggered.connect(self.schemaview.zoomOut)
        resetZoomAction.triggered.connect(self.schemaview.resetView)

        # create the list with components
        self.lwComponents = CompListWidget()
        self.lwComponents.addItem('Input')
        self.lwComponents.addItem('Output')
        self.lwComponents.addItem('Comp 2_2')
        self.lwComponents.addItem('Comp 4_4')

        self.hblLayout = QHBoxLayout()
        self.hblLayout.setSpacing(0)
        self.hblLayout.setContentsMargins(0, 0, 0, 0)
        self.hblLayout.addWidget(self.lwComponents)
        self.hblLayout.addWidget(self.schemaview)

        self.wCentrWidget = QWidget()
        self.wCentrWidget.setLayout(self.hblLayout)

        self.setCentralWidget(self.wCentrWidget)

        self.setWindowTitle('Schema designer')
        self.setGeometry(0, 30, 1300, 750)
        self.show()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName( self, 'Open schematic', './schemas')

        if filename != '':
            try:
                self.currentFile = filename
                self.schemascene.loadFromFile(self.currentFile)
                self.schemaview.setScene(self.schemascene)
                self.schemaview.resetView()
            except (FileNotFoundError, ValueError, KeyError) as e:
                QMessageBox.critical(
                    self, 'Error opening file',
                    '<b>Error opening file:</b>' + '\n\n' + str(e))

    def saveFile(self):
        self.schemascene.saveToFile(self.currentFile)

    def saveFileAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save schematic as', './schemas')
        if filename != '':
            try:
                self.schemascene.saveToFile(filename)
            except (FileNotFoundError, ValueError, KeyError) as e:
                QMessageBox.critical(
                    self, 'Error savig file',
                    '<b>Error:</b>' + '\n\n' + str(e))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/logo.png'))
    ex = MainWindow()
    app.exec_()
    app.deleteLater()
    sys.exit()
