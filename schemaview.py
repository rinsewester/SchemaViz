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

        # Create components based on graph and add them to the scene
        compdict = {}  # TODO: add better way to address components and links in scene
        for cmpname in schem.nodes():
            comp = ComponentGI(cmpname, leftSockets=schem.node[cmpname]['leftsockets'],
                rightSockets=schem.node[cmpname]['rightsockets'])
            xpos, ypos = schem.node[cmpname]['pos']
            comp.setPos(xpos, ypos)
            # TODO: add better description in tooltip after <br/>
            comp.setToolTip("<b>{}</b>".format(cmpname))
            self.addItem(comp)
            compdict[cmpname] = comp

        # Add the links as well
        for src, dst, linkattr in schem.edges(data=True):
            srccomp = compdict[src]
            dstcomp = compdict[dst]
            srcsockname = linkattr['srcoutp']
            dstsockname = linkattr['dstinp']
            if srcsockname in srccomp.leftSocketGItems.keys():
                srcsock = srccomp.leftSocketGItems[srcsockname]
            else:
                srcsock = srccomp.rightSocketGItems[srcsockname]
            if dstsockname in dstcomp.leftSocketGItems.keys():
                dstsock = dstcomp.leftSocketGItems[dstsockname]
            else:
                dstsock = dstcomp.rightSocketGItems[dstsockname]
            link = LinkGI('', srcsock, dstsock)
            self.addItem(link)
        
        # Update the scene bounding rectangle for a full view of the schematic
        self.updateSceneRect()

    def updateSceneRect(self):
        # Is called when there is a change in the scene
        # Update scene size to fit the current layout of the graph
        rect = self.itemsBoundingRect()
        rect = QRectF(rect.x() - 50, rect.y() - 50, rect.width() + 100, rect.height() + 100)
        self.setSceneRect(rect)
