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

        # dicts to keep refs to components and links:
        self.components = {}
        self.links = {}

    def addComponent(self, comp):
        self.addItem(comp)
        self.components[comp.name] = comp

    def addLink(self, link):
        self.addItem(link)
        self.links[link.name] = link

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, schemastyle.BACKGROUND_COLOR)


    # TODO add function like setSchema to keep schema object alive or 
    #   easy graph operations like find successors and DFS algorithms
    def loadFromFile(self, filename):
        schem = Schematic()
        schem.loadFromFile(filename)

        # remove all items from the scene
        self.clear()

        # Create components based on graph and add them to the scene
        for cmpname in schem.nodes():
            comp = ComponentGI(cmpname, leftSockets=schem.node[cmpname]['leftsockets'],
                rightSockets=schem.node[cmpname]['rightsockets'])
            comp.location = schem.node[cmpname]['pos']
            # TODO: add better description in tooltip after <br/>
            comp.setToolTip("<b>{}</b><br/>pos: {}".format(cmpname, comp.location))
            self.addComponent(comp)

        # Add the links as well
        for src, dst, linkattr in schem.edges(data=True):
            srccomp = self.components[src]
            dstcomp = self.components[dst]
            name = linkattr['name']
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
            link = LinkGI(name, srcsock, dstsock)
            link.thickness = 2
            self.addLink(link)
        
        # Update the scene bounding rectangle for a full view of the schematic
        self.updateSceneRect()

    def saveToFile(self, filename):
        schem = Schematic()

        for compgi in self.components.values():
            leftSocketNames = []
            for lsi in compgi.leftSocketGItems.values():
                leftSocketNames.append(lsi.name)
            rightSocketNames = []
            for rsi in compgi.rightSocketGItems.values():
                rightSocketNames.append(rsi.name)
            schem.add_component(compgi.name, leftsockets=leftSocketNames, rightsockets=rightSocketNames, pos=compgi.location)

        for linkgi in self.links.values():
            srcSocketname = linkgi.srcSocket.name
            dstSocketname = linkgi.dstSocket.name
            srcCompname = linkgi.srcSocket.parentComp.name
            dstCompname = linkgi.dstSocket.parentComp.name
            schem.add_link(srcCompname, dstCompname, srcSocketname, dstSocketname, name=linkgi.name)

        print("storing schematic to file:", filename)
        schem.storeToFile(filename)

    def updateSceneRect(self):
        # Is called when there is a change in the scene
        # Update scene size to fit the current layout of the graph
        rect = self.itemsBoundingRect()
        rect = QRectF(rect.x() - 50, rect.y() - 50, rect.width() + 100, rect.height() + 100)
        self.setSceneRect(rect)
