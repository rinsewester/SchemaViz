#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
GraphicsItem to model a socket

author: Rinse Wester

"""

import sys
from PyQt5.QtWidgets import QWidget, QGraphicsItem, QPushButton, QVBoxLayout, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import QRectF, QRect, QPointF, QPoint, Qt, QVariant
from PyQt5.QtGui import QColor, QPainter, QBrush, QPainterPath, QLinearGradient, QFont, QContextMenuEvent
from collections import Counter
import schemastyle

class SocketGI(QGraphicsItem):

    LEFT = 0
    RIGHT = 1

    def __init__(self, name, location):
        super().__init__()
        
        self.sockWidth = 50
        self.sockHeight = 20

        self.setAcceptHoverEvents(True)
        self.hovering = False

        self.sockName = name
        self.sockLocation = location

    def boundingRect(self):
        return QRectF(0, -self.sockHeight // 2, self.sockWidth, self.sockHeight)
    
    def paint(self, painter, option, widget):
        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        
        if lod > 0.4:
            # Draw in high detail
            painter.drawRoundedRect(0, -self.compHeight // 2,
                self.compWidth, self.compHeight, 3, 3)
        else:
            # Draw in low detail
            painter.drawRect(0, -self.compHeight // 2,
                self.compWidth, self.compHeight)

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.CrossCursor)
        self.hovering = True
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hovering = False
        super().hoverLeaveEvent(event)

            
    