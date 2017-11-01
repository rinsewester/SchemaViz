#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
GraphicsItem to model a link

author: Rinse Wester

"""

import sys
from PyQt5.QtWidgets import QWidget, QGraphicsItem, QGraphicsPathItem, QMenu, QAction
from PyQt5.QtCore import QRectF, QRect, QPointF, QPoint, Qt, QVariant
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath, QFont
from collections import Counter
import schemastyle

class LinkGI(QGraphicsPathItem):

    def __init__(self, name, srcSocket, dstSocket):
        super().__init__()

        self.setAcceptHoverEvents(True)
        self.hovering = False

        self.linkName = name
        self.srcSocket = srcSocket
        self.dstSocket = dstSocket
        self.srcX, self.srcY = srcSocket.linkConnectionPos()
        self.dstX, self.dstY = dstSocket.linkConnectionPos()
        self.sockBRect = QRectF(min(self.srcX, self.dstX), min(self.srcY, self.dstY),
            abs(self.srcX - self.dstX), abs(self.srcY - self.dstY))

        # Create the bezier curve path
        self.linkPath = QPainterPath()
        self.linkPath.moveTo(self.srcX, self.srcY)
        self.linkPath.cubicTo(self.srcX + 128, self.srcY, self.dstX - 128, self.dstY, self.dstX, self.dstY)
        self.setPath(self.linkPath)

        # set the pen style
        self.linkPen = QPen()
        self.linkPen.setWidth(4)
        self.linkPen.setCapStyle(Qt.RoundCap);
        self.linkPen.setColor(QColor(Qt.gray))
        self.setPen(self.linkPen)

    def hoverEnterEvent(self, event):
        self.linkPen.setColor(QColor(Qt.white))
        self.setPen(self.linkPen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.linkPen.setColor(QColor(Qt.gray))
        self.setPen(self.linkPen)
        super().hoverLeaveEvent(event)

            
    