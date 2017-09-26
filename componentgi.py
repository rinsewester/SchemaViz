#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
GraphicsItem to model a component

author: Rinse Wester

"""

import sys
from PyQt5.QtWidgets import QWidget, QGraphicsItem, QPushButton, QVBoxLayout, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import QRectF, QRect, QPointF, QPoint, Qt, QVariant
from PyQt5.QtGui import QColor, QPainter, QBrush, QPainterPath, QLinearGradient, QFont, QContextMenuEvent
from collections import Counter
import schemastyle

class ComponentGI(QGraphicsItem):

    def __init__(self):
        super().__init__()
        
        self.compWidth = 100
        self.compHeight = 60
        self.snappingIsOn = True

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.hovering = False

    def boundingRect(self):
        return QRectF(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight)
    
    def paint(self, painter, option, widget):
        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        
        if self.isSelected():
            painter.setPen(Qt.white)
        else:
            painter.setPen(Qt.NoPen)
        if self.hovering:
            painter.setBrush(QBrush(schemastyle.NODE_BACKGROUND_COLOR.lighter(150)))
        else:
            painter.setBrush(QBrush(schemastyle.NODE_BACKGROUND_COLOR))

        if lod > 0.5:
            # Draw in high detail
            painter.drawRoundedRect(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight, 5, 5)
        else:
            # Draw in low detail
            painter.drawRect(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight)


    def hoverEnterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.hovering = True
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hovering = False
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        newPos = value
        if change == QGraphicsItem.ItemPositionChange:
            newPos = self.snapToGrid(newPos)

        return super().itemChange(change, newPos)

    def snapToGrid(self, position):
        gridSizeX = 25
        gridSizeY = 10
        curPos = QPoint(position.x(), position.y())
        return QPoint(round(curPos.x() / gridSizeX) * gridSizeX, round(curPos.y() / gridSizeY) * gridSizeY)
    
    def contextMenuEvent(self, event):
        print('node menu triggered')
        # pos = event.scenePos()
        # point = self.view.mapFromScene(pos)
        # point = self.view.mapToGlobal(point)
        # self.menu.exec(point)
            
    