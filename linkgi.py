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
        self.srcSocket.link = self
        self.dstSocket.link = self

        self.updateShape()

        # set the pen style
        self.linkPen = QPen()
        self.linkPen.setWidth(4)
        self.linkPen.setCapStyle(Qt.RoundCap);
        self.linkPen.setColor(QColor(Qt.gray))
        self.setPen(self.linkPen)

    def updateShape(self):
        # Create the bezier curve path
        srcX, srcY = self.srcSocket.linkConnectionPos()
        dstX, dstY = self.dstSocket.linkConnectionPos()
        linkPath = QPainterPath()
        linkPath.moveTo(srcX, srcY)
        linkPath.cubicTo(srcX + 128, srcY, dstX - 128, dstY, dstX, dstY)
        self.setPath(linkPath)

    def hoverEnterEvent(self, event):
        self.linkPen.setColor(QColor(Qt.white))
        self.setPen(self.linkPen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.linkPen.setColor(QColor(Qt.gray))
        self.setPen(self.linkPen)
        super().hoverLeaveEvent(event)

            
    