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

class SchemaView(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame);
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.zoomLevel = 250

    def wheelEvent(self, event):
        #Catch wheelEvent and zoom instead of scroll when Ctrl is pressed
        if event.modifiers() & Qt.ControlModifier:
            if not event.angleDelta().isNull():
                if event.angleDelta().y() > 0:
                    self.widget.zoomIn()
                else:
                    self.widget.zoomOut()
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
        self.zoomLevel = 250
        self.setupMatrix()
        self.schemaview.ensureVisible(QRectF(0,0,0,0))

    def setupMatrix(self):
        scale = 2.0 ** ((self.zoomLevel - 250) / 50.0)
        transform = QTransform()
        transform.scale(scale, scale)
        self.schemaview.setTransform(transform)

    def zoomIn(self):
        self.zoomLevel += 10
        if self.zoomLevel > 350:
            self.zoomLevel = 350
        self.setupMatrix()

    def zoomOut(self):
        self.zoomLevel -= 10
        if self.zoomLevel < 0:
            self.zoomLevel = 0
        self.setupMatrix()


class SchemaScene(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.lockScene = False
        self.changed.connect(self.updateSceneRect)

    def drawBackground(self, painter, rect):
        painter.fillRect(rect, schemastyle.BACKGROUND_COLOR)

    def updateSceneRect(self):
        # Is called when there is a change in the scene
        # Update scene size to fit the current layout of the graph
        if not self.lockScene:
            rect = self.itemsBoundingRect()
            rect = QRectF(rect.x() - 50, rect.y() - 50, rect.width() + 100, rect.height() + 100)
            self.setSceneRect(rect)
        else:
            self.lockScene = False

class GraphWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        self.schemaview = SchemaView(self)

        #Make a graphics scene
        self.scene = GraphicsScene()
        self.schemaview.setScene(self.scene)

        #Final layout
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(0)
        topLayout.addWidget(self.schemaview)
        self.setLayout(topLayout)


    def setStaticGraph(self):

        minX, minY, maxX, maxY = -50, -50, 150, 100
        self.centerOfGraph = QPointF((minX + maxX) / 2, (minY + maxY) / 2)

        self.graph.clearGraph()
        self.scene.clear()


        #Place graph objects based on the graph data
        nodeList = []
        nodePoints = []
        
        n1_name, n1_x, n1_y = 'N1', 100, 100
        n2_name, n2_x, n2_y = 'N2', 250, 100
        n3_name, n3_x, n3_y = 'N3', 250, 200

        self.graph.addNode(n1_name, n1_x, n1_y)
        nodeList.append(n1_name)
        nodePoints.append([n1_x, n1_y])
        self.graph.addNode(n2_name, n2_x, n2_y)
        nodeList.append(n2_name)
        nodePoints.append([n2_x, n2_y])
        self.graph.addNode(n3_name, n3_x, n3_y)
        nodeList.append(n3_name)
        nodePoints.append([n3_x, n3_y])

        # PLace the edges
        n1_idx = 0
        n2_idx = 1
        n3_idx = 2
        self.graph.addEdgeToNodes(n1_idx, n2_idx, 'right', 'left', src = 'N1', dst = 'N2')
        self.graph.addEdgeToNodes(n2_idx, n1_idx, 'left', 'right', src = 'N2', dst = 'N1')
        self.graph.addEdgeToNodes(n1_idx, n3_idx, 'right', 'left', src = 'N1', dst = 'N3')

        self.scene.updateSceneRect()
        self.resetView()
        self.update()
