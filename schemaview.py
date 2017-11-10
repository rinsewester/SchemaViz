#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Widget to display a schema

author: Rinse Wester

"""

import sys

from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QTransform, QPainter, QColor, QPalette

import schemastyle
from schematic import Schematic
from componentgi import ComponentGI
from linkgi import LinkGI

class SchemaView(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame);
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing, True)

        self.minZoomLevel = 0
        self.maxZoomLevel = 400
        self.defaultZoomLevel = 200

        self.resetView()

    def wheelEvent(self, event):
        #Catch wheelEvent and zoom instead of scroll when Ctrl is pressed
        if event.modifiers() & Qt.ControlModifier:
            if not event.angleDelta().isNull():
                if event.angleDelta().y() > 0:
                    self.zoomIn()
                else:
                    self.zoomOut()
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier:
            self.setInteractive(False)
            self.setDragMode(True)           

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.setInteractive(True)
        self.setDragMode(False)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        super().keyReleaseEvent(event)

    def resetView(self):
        self.zoomLevel = self.defaultZoomLevel
        self.setupMatrix()
        self.ensureVisible(QRectF(0, 0, 0, 0))

    def setupMatrix(self):
        scale = 2.0 ** ((self.zoomLevel - self.maxZoomLevel // 2) / 100.0)
        transform = QTransform()
        transform.scale(scale, scale)
        self.setTransform(transform)

    def zoomIn(self):
        self.zoomLevel += 10
        if self.zoomLevel > self.maxZoomLevel:
            self.zoomLevel = self.maxZoomLevel
        self.setupMatrix()

    def zoomOut(self):
        self.zoomLevel -= 10
        if self.zoomLevel < self.minZoomLevel:
            self.zoomLevel = self.minZoomLevel
        self.setupMatrix()


class SchemaScene(QGraphicsScene):

    def __init__(self):
        super().__init__()
        # self.changed.connect(self.updateSceneRect)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, schemastyle.BACKGROUND_COLOR)

    def loadFromFile(self, filename):
        schem = Schematic()
        schem.loadFromFile(filename)

        # remove all items from the scene
        self.clear()

        for cmpname in schem.nodes():
            comp = ComponentGI(cmpname, leftSockets=schem.node[cmpname]['leftsockets'],
                rightSockets=schem.node[cmpname]['rightsockets'])
            comp.setPos(400, 400)
            # comp.setToolTip("<b>{}</b><br/>more info".format(cmpname))
            self.addItem(comp)

        # Add some components
        comp0 = ComponentGI('comp 0', leftSockets=['In'], rightSockets=['Out0', 'Out1'])
        comp0.setPos(0, 0)
        self.addItem(comp0)
        comp1 = ComponentGI('comp 1', leftSockets=['In'], rightSockets=['Out'])
        comp1.setPos(250, -100)
        self.addItem(comp1)
        comp2 = ComponentGI('comp 2', leftSockets=['In0', 'In1'], rightSockets=['Out'])
        comp2.setPos(500, 0)
        self.addItem(comp2)
        comp3 = ComponentGI('comp 3', leftSockets=['In'], rightSockets=['Out'])
        comp3.setPos(700, 0)
        self.addItem(comp3)

        # Add the links between components
        link0 = LinkGI('link 0', comp0.rightSocketGItems['Out0'], comp1.leftSocketGItems['In'])
        self.addItem(link0)
        link1 = LinkGI('link 1', comp1.rightSocketGItems['Out'], comp2.leftSocketGItems['In0'])
        self.addItem(link1)
        link2 = LinkGI('link 2', comp0.rightSocketGItems['Out1'], comp2.leftSocketGItems['In1'])
        self.addItem(link2)
        link3 = LinkGI('link 3', comp2.rightSocketGItems['Out'], comp3.leftSocketGItems['In'])
        self.addItem(link3)
        
        # Update the scene bounding rectangle for a full view of the schematic
        self.updateSceneRect()

    def updateSceneRect(self):
        # Is called when there is a change in the scene
        # Update scene size to fit the current layout of the graph
        rect = self.itemsBoundingRect()
        rect = QRectF(rect.x() - 50, rect.y() - 50, rect.width() + 100, rect.height() + 100)
        self.setSceneRect(rect)
