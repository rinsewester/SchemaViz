#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mainwindow of SDFkit showing all widgets.

author: Rinse Wester

"""

import sys
from PyQt5.QtWidgets import QDockWidget, QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, qApp
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from schemaview import SchemaView, SchemaScene
import schemastyle

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

        exitAction = QAction(QIcon('images/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        graphmenu = self.menuBar().addMenu('&Graph')
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

        self.schemaview = SchemaView()
        self.schemascene = SchemaScene()
        self.schemascene.loadFromFile(MainWindow.DEFAULT_FILE)
        self.schemaview.setScene(self.schemascene)
        self.schemaview.resetView()

        # connect the view menu actions to the graphwidget
        zoomInAction.triggered.connect(self.schemaview.zoomIn)
        zoomOutAction.triggered.connect(self.schemaview.zoomOut)
        resetZoomAction.triggered.connect(self.schemaview.resetView)

        self.setCentralWidget(self.schemaview)

        self.setWindowTitle('Schema designer')
        self.setGeometry(0, 30, 1300, 750)
        self.show()

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName( self, 'Open schematic', './schemas')

        if filename != '':
            try:
                self.schemascene.loadFromFile(filename)
                self.schemaview.setScene(self.schemascene)
                self.schemaview.resetView()
            except (FileNotFoundError, ValueError, KeyError) as e:
                QMessageBox.critical(
                    self, 'Error opening file',
                    '<b>Error opening file:</b>' + '\n\n' + str(e))

    def saveFile(self):
        self.schemascene.saveToFile(MainWindow.DEFAULT_FILE+'.saved')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/logo.png'))
    ex = MainWindow()
    app.exec_()
    app.deleteLater()
    sys.exit()
