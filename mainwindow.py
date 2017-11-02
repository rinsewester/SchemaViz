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
from componentgi import ComponentGI
from socketgi import SocketGI
from linkgi import LinkGI
import schemastyle

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        openAction = QAction(QIcon('images/open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open schematic')
        openAction.triggered.connect(self.openFile)

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

        # Use mac unitfied toolbar when running on mac
        if sys.platform == 'darwin':
            self.setUnifiedTitleAndToolBarOnMac(True)

        self.schemaview = SchemaView()
        self.schemascene = SchemaScene()

        # Add a few compoents
        comp0 = ComponentGI('comp 0', leftSockets=['In'], rightSockets=['Out0', 'Out1'])
        comp0.setPos(0, 0)
        self.schemascene.addItem(comp0)
        comp1 = ComponentGI('comp 1', leftSockets=['In'], rightSockets=['Out'])
        comp1.setPos(250, -100)
        self.schemascene.addItem(comp1)
        comp2 = ComponentGI('comp 2', leftSockets=['In0', 'In1'], rightSockets=['Out'])
        comp2.setPos(500, 0)
        self.schemascene.addItem(comp2)
        comp3 = ComponentGI('comp 3', leftSockets=['In'], rightSockets=['Out'])
        comp3.setPos(700, 0)
        self.schemascene.addItem(comp3)

        link0 = LinkGI('link 0', comp0.rightSocketGItems['Out0'], comp1.leftSocketGItems['In'])
        link1 = LinkGI('link 1', comp1.rightSocketGItems['Out'], comp2.leftSocketGItems['In0'])
        link2 = LinkGI('link 2', comp0.rightSocketGItems['Out1'], comp2.leftSocketGItems['In1'])
        link3 = LinkGI('link 3', comp2.rightSocketGItems['Out'], comp3.leftSocketGItems['In'])
        self.schemascene.addItem(link0)
        self.schemascene.addItem(link1)
        self.schemascene.addItem(link2)
        self.schemascene.addItem(link3)

        self.schemascene.updateSceneRect()
        self.schemaview.setScene(self.schemascene)
        self.schemaview.resetView()
        self.schemaview.update()

        # connect the view menu actions to the graphwidget
        zoomInAction.triggered.connect(self.schemaview.zoomIn)
        zoomOutAction.triggered.connect(self.schemaview.zoomOut)
        resetZoomAction.triggered.connect(self.schemaview.resetView)

        self.setCentralWidget(self.schemaview)

        self.setWindowTitle('Schema designer')
        self.setGeometry(0, 30, 1300, 750)
        self.show()

    def openFile(self):
        print('open file....')

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/logo.png'))
    ex = MainWindow()
    app.exec_()
    app.deleteLater()
    sys.exit()
