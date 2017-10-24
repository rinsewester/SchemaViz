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

    def __init__(self, name):
        super().__init__()
        
        self.compWidth = 200
        self.compHeight = 100
        self.snappingIsOn = True

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.hovering = False

        self.compName = name

    def boundingRect(self):
        return QRectF(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight)
    
    def paint(self, painter, option, widget):
        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        
        if self.isSelected():
            painter.setPen(Qt.white)
        else:
            painter.setPen(Qt.NoPen)
        if self.hovering:
            painter.setBrush(QBrush(schemastyle.COMPONENT_BACKGROUND_COLOR.lighter(150)))
        else:
            painter.setBrush(QBrush(schemastyle.COMPONENT_BACKGROUND_COLOR))

        if lod > 0.4:
            # Draw in high detail
            painter.drawRoundedRect(-self.compWidth // 2, -self.compHeight // 2,
                self.compWidth, self.compHeight, 5, 5)

            textrect = QRectF(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight)
            painter.setPen(schemastyle.COMPONENT_TEXT_COLOR)
            painter.drawText(textrect, Qt.AlignCenter, self.compName)
        else:
            # Draw in low detail
            painter.drawRect(-self.compWidth // 2, -self.compHeight // 2,
                self.compWidth, self.compHeight)


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
        cur_x, cur_y = position.x(), position.y()
        return QPoint(round(cur_x / schemastyle.GRID_X_RES) * schemastyle.GRID_X_RES,
            round(cur_y / schemastyle.GRID_Y_RES) * schemastyle.GRID_Y_RES)
    
    def contextMenuEvent(self, event):
        print('COMPONENT menu triggered')
        # pos = event.scenePos()
        # point = self.view.mapFromScene(pos)
        # point = self.view.mapToGlobal(point)
        # self.menu.exec(point)
            
    