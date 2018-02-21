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

    def __init__(self, name, location, parent):
        super().__init__()

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        
        self.sockWidth = 50
        self.sockHeight = 20

        self.sockName = name
        self.sockLocation = location
        self.parentComp = parent
        self.link = None
        self.hovering = False

        if self.sockLocation == SocketGI.LEFT:
            self.sockBRect = QRectF(0, -self.sockHeight // 2, self.sockWidth, self.sockHeight)
        else:
            self.sockBRect = QRectF(-self.sockWidth, -self.sockHeight // 2, self.sockWidth, self.sockHeight)

    def boundingRect(self):
        return self.sockBRect
    
    def paint(self, painter, option, widget):
        # Draw in high detail
        painter.setPen(Qt.NoPen)
        if self.hovering:
            painter.setBrush(QBrush(schemastyle.SOCKET_CONNECTED_COLOR))
            rad = 7
        else:
            painter.setBrush(QBrush(schemastyle.SOCKET_NEUTRAL_COLOR))
            rad = 6
        oldfont = painter.font()
        font = QFont(oldfont)
        font.setPixelSize(10)
        painter.setFont(font)
        if self.sockLocation == SocketGI.LEFT:
            painter.drawEllipse(QPoint(self.sockHeight // 2, 0), rad, rad)
            textrect = QRectF(self.sockHeight, -self.sockHeight // 2, self.sockWidth - self.sockHeight, self.sockHeight)
            painter.setPen(schemastyle.SOCKET_NAME_COLOR)
            painter.drawText(textrect, Qt.AlignLeft | Qt.AlignVCenter, self.sockName)
        else:
            painter.drawEllipse(QPoint(-self.sockHeight // 2, 0), rad, rad)
            textrect = QRectF(-self.sockWidth, -self.sockHeight // 2, self.sockWidth - self.sockHeight, self.sockHeight)
            painter.setPen(schemastyle.SOCKET_NAME_COLOR)
            painter.drawText(textrect, Qt.AlignRight | Qt.AlignVCenter, self.sockName)

        # restore font
        painter.setFont(oldfont)

    def onSockConn(self, pos):
        if self.sockLocation == SocketGI.LEFT:
            return pos.x() < self.sockHeight
        else:
            return pos.x() > -self.sockHeight

    def hoverMoveEvent(self, event):
        if self.onSockConn(event.pos()):
            self.hovering = True
            self.setCursor(Qt.CrossCursor)
        else:
            self.hovering = False
            self.setCursor(Qt.ArrowCursor)
        self.update()

    def mousePressEvent(self, event):
        if self.onSockConn(event.pos()) and self.link == None:
            if self.scene().nowConnecting:
                canConnect = True
                if canConnect:
                    self.scene().finishConnecting(self)
            else:
                self.scene().startConnecting(self)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.hovering = False
        super().hoverLeaveEvent(event)

    def linkConnectionPos(self):
        if self.sockLocation == SocketGI.LEFT:
            scnpos = self.mapToScene(self.sockHeight / 2.0, 0.0)
            return scnpos.x(), scnpos.y()
        else:
            scnpos = self.mapToScene(-self.sockHeight / 2.0, 0.0)
            return scnpos.x(), scnpos.y()

    @property
    def name(self):
        return self.sockName

    @name.setter
    def name(self, name):
        self.sockName = name
        self.update()


