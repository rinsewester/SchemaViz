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
        self.toolbar.addAction(exitAction)

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

        link0 = LinkGI('link 0',
            comp0.rightSocketGItems[0].linkConnectionPos(),
            comp1.leftSocketGItems[0].linkConnectionPos())
        link1 = LinkGI('link 1',
            comp1.rightSocketGItems[0].linkConnectionPos(),
            comp2.leftSocketGItems[0].linkConnectionPos())
        link2 = LinkGI('link 2',
            comp0.rightSocketGItems[1].linkConnectionPos(),
            comp2.leftSocketGItems[1].linkConnectionPos())
        self.schemascene.addItem(link0)
        self.schemascene.addItem(link1)
        self.schemascene.addItem(link2)

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

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/logo.png'))
    ex = MainWindow()
    app.exec_()
    app.deleteLater()
    sys.exit()
