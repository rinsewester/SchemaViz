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

        if self.sockLocation == SocketGI.LEFT:
            self.sockBRect = QRectF(0, -self.sockHeight // 2, self.sockWidth, self.sockHeight)
        else:
            self.sockBRect = QRectF(-self.sockWidth, -self.sockHeight // 2, self.sockWidth, self.sockHeight)


    def boundingRect(self):
        return self.sockBRect
    
    def paint(self, painter, option, widget):
        # Draw in high detail
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(schemastyle.SOCKET_NEUTRAL_COLOR))
        oldfont = painter.font()
        font = QFont(oldfont)
        font.setPixelSize(10)
        painter.setFont(font)
        if self.sockLocation == SocketGI.LEFT:
            painter.drawEllipse(QPoint(self.sockHeight // 2, 0), 6, 6)
            textrect = QRectF(self.sockHeight, -self.sockHeight // 2, self.sockWidth - self.sockHeight, self.sockHeight)
            textrect.translate(0, 4)
            painter.setPen(schemastyle.SOCKET_NAME_COLOR)
            painter.drawText(textrect, Qt.AlignLeft, self.sockName)
        else:
            painter.drawEllipse(QPoint(-self.sockHeight // 2, 0), 6, 6)
            textrect = QRectF(-self.sockWidth, -self.sockHeight // 2, self.sockWidth - self.sockHeight, self.sockHeight)
            textrect.translate(0, 4)
            painter.setPen(schemastyle.SOCKET_NAME_COLOR)
            painter.drawText(textrect, Qt.AlignRight, self.sockName)

        # restore font
        painter.setFont(oldfont)
        

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.CrossCursor)
        self.hovering = True
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hovering = False
        super().hoverLeaveEvent(event)

            
    