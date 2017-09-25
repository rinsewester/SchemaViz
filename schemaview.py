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
        self.zoomLevel = 250
        self.setupMatrix()
        self.ensureVisible(QRectF(0,0,0,0))

    def setupMatrix(self):
        scale = 2.0 ** ((self.zoomLevel - 250) / 50.0)
        transform = QTransform()
        transform.scale(scale, scale)
        self.setTransform(transform)

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
