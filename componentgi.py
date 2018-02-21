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
from collections import Counter, OrderedDict
from socketgi import SocketGI
import schemastyle

class ComponentGI(QGraphicsItem):

    def __init__(self, name, leftSockets=[], rightSockets=[]):
        super().__init__()
        
        self.compWidth = 150
        self.compHeight = max(len(leftSockets), len(rightSockets)) * 20 + 20# 50
        self.snappingIsOn = True

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.hovering = False

        self.compName = name
        self.leftSocketGItems = OrderedDict()
        self.rightSocketGItems = OrderedDict()

        # Create sockets for the left side
        for ind, lsn in enumerate(leftSockets):
            lsockGItem = SocketGI(lsn, SocketGI.LEFT, self)
            hoffs = -(len(leftSockets) - 1) * 20 // 2
            lsockGItem.moveBy(-self.compWidth // 2, hoffs + ind * 20)
            lsockGItem.setParentItem(self)
            self.leftSocketGItems[lsn] = lsockGItem

        # Create sockets for the right side
        for ind, rsn in enumerate(rightSockets):
            rsockGItem = SocketGI(rsn, SocketGI.RIGHT, self)
            hoffs = -(len(rightSockets) - 1) * 20 // 2
            rsockGItem.moveBy(self.compWidth // 2, hoffs + ind * 20)
            rsockGItem.setParentItem(self)
            self.rightSocketGItems[rsn] = rsockGItem

    @property
    def name(self):
        return self.compName

    @name.setter
    def name(self, name):
        self.compName = name
        self.update()

    @property
    def location(self):
        return self.x(), self.y()

    @location.setter
    def location(self, location):
        x, y = location
        self.setPos(x, y)

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
        self.hovering = True
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovering = False
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        newPos = value
        if change == QGraphicsItem.ItemPositionChange:
            newPos = self.snapToGrid(newPos)
            # update all the links such that the postions of the src/dst matches with the socket
            for sock in self.leftSocketGItems.values():
                if sock.link is not None:
                    sock.link.updateShape()
            for sock in self.rightSocketGItems.values():
                if sock.link is not None:
                    sock.link.updateShape()
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
            
    