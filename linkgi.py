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

    def __init__(self, name, srcSocket, dstSocket, thickness=2):
        super().__init__()

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
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
        self.linkPen.setWidth(thickness)
        self.linkPen.setCapStyle(Qt.RoundCap);
        self.linkPen.setColor(schemastyle.LINK_COLOR)
        self.setPen(self.linkPen)

    def updateShape(self):
        # Create the bezier curve path
        srcX, srcY = self.srcSocket.linkConnectionPos()
        dstX, dstY = self.dstSocket.linkConnectionPos()
        linkPath = QPainterPath()
        linkPath.setFillRule(Qt.WindingFill)
        linkPath.moveTo(srcX, srcY)
        linkPath.cubicTo(srcX + 100, srcY, dstX - 100, dstY, dstX, dstY)
        
        self.setPath(linkPath)

    def hoverEnterEvent(self, event):
        self.linkPen.setColor(QColor(Qt.white))
        self.setPen(self.linkPen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.linkPen.setColor(QColor(Qt.gray))
        self.setPen(self.linkPen)
        super().hoverLeaveEvent(event)

    @property
    def name(self):
        return self.linkName

    @name.setter
    def name(self, name):
        self.linkName = name
        self.update()

    @property
    def thickness(self):
        return self.linkPen.width()

    @thickness.setter
    def thickness(self, thickness):
        self.linkPen.setWidth(thickness)
        self.setPen(self.linkPen)
        self.update()


class PartialLinkGI(QGraphicsPathItem):

    def __init__(self, dstTempPos=(0, 0)):
        super().__init__()

        self.dstTempPos = dstTempPos

        # set the pen style
        self.linkPen = QPen()
        self.linkPen.setWidth(2)
        self.linkPen.setCapStyle(Qt.RoundCap);
        self.linkPen.setColor(schemastyle.LINK_COLOR)
        self.setPen(self.linkPen)

    def setSourceSocket(self, srcSock):
        self.srcSocket = srcSock
        self.srcSocket.link = self
        self.updateShape()

    def setDestTempPos(self, xpos, ypos):
        self.dstTempPos = xpos, ypos
        self.updateShape()

    def updateShape(self):
        # Create the bezier curve path
        srcX, srcY = self.srcSocket.linkConnectionPos()
        dstX, dstY = self.dstTempPos
        linkPath = QPainterPath()
        linkPath.setFillRule(Qt.WindingFill)
        linkPath.moveTo(srcX, srcY)
        linkPath.cubicTo(srcX + 100, srcY, dstX - 100, dstY, dstX, dstY)
        
        self.setPath(linkPath)

