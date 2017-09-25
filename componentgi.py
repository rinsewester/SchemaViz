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

    def boundingRect(self):
        return QRectF(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight)
    
    def paint(self, painter, option, widget):
        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        
        painter.setPen(Qt.NoPen)
        if self.isSelected():
            painter.setBrush(QBrush(Qt.gray))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRoundedRect(-self.compWidth // 2, -self.compHeight // 2, self.compWidth, self.compHeight, 5, 5)

        # if lod > 0.2:
        #     self.paintNodeIO(painter, lod)
        # if lod > 0.4:
        #     self.paintNodeName(painter)


    # def itemChange(self, change, value):
    #     newPos = value
    #     if change == QGraphicsItem.ItemPositionChange:
    #         newPos = self.snapToGrid(newPos)

    #     return super().itemChange(change, newPos)

    # def snapToGrid(self, position):
    #     gridSizeX = 40
    #     gridSizeY = 10
    #     curPos = QPoint(position.x(), position.y())
    #     return QPoint(round(curPos.x() / gridSizeX) * gridSizeX, round(curPos.y() / gridSizeY) * gridSizeY)
    
    def contextMenuEvent(self, event):
        print('node menu triggered')
        # pos = event.scenePos()
        # point = self.view.mapFromScene(pos)
        # point = self.view.mapToGlobal(point)
        # self.menu.exec(point)
            
    