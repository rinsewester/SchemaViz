#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Widget to display simulation data of a CSDF graph.

author: Sander Giesselink

"""

import sys
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QHBoxLayout, QFrame, QGLWidget
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QTransform, QPainter, QColor, QPalette
from graph import Graph
import schemastyle

class GraphicsView(QGraphicsView):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        
        # Remove ugly one pixel border by changing the framestyle
        self.setFrameStyle(QFrame.NoFrame);

        # use openGL to accelerate painting:
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setOptimizationFlags(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))

    def wheelEvent(self, event):
        #Catch wheelEvent and zoom instead of scroll when Ctrl is pressed
        if event.modifiers() & Qt.ControlModifier:
            if not event.angleDelta().isNull():
                if event.angleDelta().y() > 0:
                    self.widget.zoomIn()
                else:
                    self.widget.zoomOut()
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ShiftModifier:
            self.setInteractive(False)
            self.setDragMode(True)           

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        self.setInteractive(True)
        self.setDragMode(False)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        super().keyReleaseEvent(event)


class GraphicsScene(QGraphicsScene):

    def __init__(self):
        super().__init__()

        self.drawGrid = True
        self.lockScene = False

        self.changed.connect(self.updateSceneRect)

    def drawBackground(self, painter, rect):

        painter.fillRect(rect, schemastyle.BACKGROUND_COLOR)

        if self.drawGrid:
            painter.setPen(schemastyle.GRID_COLOR)

            xGridSize = 512
            yGridSize = 512
            gridSizeX = 40
            gridSizeY = 20
            
            for i in range(yGridSize * 2):
                y = i * gridSizeY - (yGridSize) * gridSizeY
                painter.drawLine(-xGridSize * gridSizeX, y, xGridSize * gridSizeX, y)

            for i in range(xGridSize * 2):
                x = i * gridSizeX  - (xGridSize) * gridSizeX
                painter.drawLine(x, -yGridSize * gridSizeY, x, yGridSize * gridSizeY)

    def updateSceneRect(self):
        #Is called when there is a change in the scene
        #Update scene size to fit the current layout of the graph
        if not self.lockScene:
            rect = self.itemsBoundingRect()
            rect = QRectF(rect.x() - 50, rect.y() - 50, rect.width() + 100, rect.height() + 100)
            self.setSceneRect(rect)
        else:
            self.lockScene = False

class GraphWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        
    def initUI(self):
        self.graphicsView = GraphicsView(self)

        #Make a graphics scene
        self.scene = GraphicsScene()
        self.graphicsView.setScene(self.scene)

        #Create a graph that can contain nodes and edges
        self.graph = Graph(self, self.scene, self.graphicsView)

        # initial zoomlevel
        self.zoomLevel = 250

        #Final layout
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSpacing(0)
        topLayout.addWidget(self.graphicsView)
        self.setLayout(topLayout)


    def setStaticGraph(self):

        minX, minY, maxX, maxY = -50, -50, 150, 100
        self.centerOfGraph = QPointF((minX + maxX) / 2, (minY + maxY) / 2)

        self.graph.clearGraph()
        self.scene.clear()


        #Place graph objects based on the graph data
        nodeList = []
        nodePoints = []
        
        n1_name, n1_x, n1_y = 'N1', 100, 100
        n2_name, n2_x, n2_y = 'N2', 250, 100
        n3_name, n3_x, n3_y = 'N3', 250, 200

        self.graph.addNode(n1_name, n1_x, n1_y)
        nodeList.append(n1_name)
        nodePoints.append([n1_x, n1_y])
        self.graph.addNode(n2_name, n2_x, n2_y)
        nodeList.append(n2_name)
        nodePoints.append([n2_x, n2_y])
        self.graph.addNode(n3_name, n3_x, n3_y)
        nodeList.append(n3_name)
        nodePoints.append([n3_x, n3_y])

        # PLace the edges
        n1_idx = 0
        n2_idx = 1
        n3_idx = 2
        self.graph.addEdgeToNodes(n1_idx, n2_idx, 'right', 'left', src = 'N1', dst = 'N2')
        self.graph.addEdgeToNodes(n2_idx, n1_idx, 'left', 'right', src = 'N2', dst = 'N1')
        self.graph.addEdgeToNodes(n1_idx, n3_idx, 'right', 'left', src = 'N1', dst = 'N3')



        self.scene.updateSceneRect()
        self.resetView()
        self.update()

    def setGraph(self, graphData):
        if graphData != None:
            self.graphData = graphData

            # set widget size based on min/max positions of nodes
            if not self.graphData is None:
                minX, minY = sys.maxsize, sys.maxsize
                maxX, maxY = 0, 0
                for n in self.graphData.nodes():
                    x, y = self.graphData.node[n]['pos']
                    minX = min(minX, x - 50)
                    minY = min(minY, y - 50)
                    maxX = max(maxX, x + 50)
                    maxY = max(maxY, y + 50)

                # Determine the center of the graph
                self.centerOfGraph = QPointF((minX + maxX) / 2, (minY + maxY) / 2)

            self.placeGraphObjects()

            #Resize scene to be slightly larger than the graph
            self.scene.updateSceneRect()

            self.resetView()
            self.update()
     
    def placeGraphObjects(self):
        
        self.graph.clearGraph()
        self.scene.clear()

        #Place graph objects based on the graph data
        nodeList = []
        nodePoints = []
        for n in self.graphData.nodes():
            #Place nodes
            x, y = self.graphData.node[n]['pos']
            func = self.graphData.node[n]['funcstr']
            clashCode = self.graphData.node[n]['clashcode']
            r, g, b = self.graphData.node[n]['color']

            self.graph.addNode1_n  (n, x, y)
            nPoint = [x, y]
            nodeList.append(n)
            nodePoints.append(nPoint)

        #Check for self-looping edges first
        for src, dst in self.graphData.edges():
            #Place edges and tokens
            node1 = nodeList.index(src)
            node2 = nodeList.index(dst)
            
            if src == dst:
                tokenValues = self.graphData[src][dst]['tkns']
                pRates = self.graphData[src][dst]['prates']
                cRates = self.graphData[src][dst]['crates']
                resnr = self.graphData[src][dst]['res']
                argnr = self.graphData[src][dst]['arg']
                r, g, b = self.graphData[src][dst]['color']
                color = QColor(r, g, b)
                    
                self.graph.addEdgeToNodes(node1, node2, 'right', 'left', src, dst, tokenValues, pRates, cRates, resnr, argnr, color)
                
        #Then place the rest of the edges (not self-looping)
        for src, dst in self.graphData.edges():
            #Place edges and tokens
            node1 = nodeList.index(src)
            node2 = nodeList.index(dst)
            
            if src != dst:
                tokenValues = self.graphData[src][dst]['tkns']
                pRates = self.graphData[src][dst]['prates']
                cRates = self.graphData[src][dst]['crates']
                resnr = self.graphData[src][dst]['res']
                argnr = self.graphData[src][dst]['arg']
                r, g, b = self.graphData[src][dst]['color']
                color = QColor(r, g, b)
                self.tokensInScene.append((src, dst))    

                #If begin node is left of end node
                if nodePoints[node1][0] < nodePoints[node2][0]:
                    self.graph.addEdgeToNodes(node1, node2, 'right', 'left', src, dst, tokenValues, pRates, cRates, resnr, argnr, color)
                elif nodePoints[node1][0] > nodePoints[node2][0]:
                    self.graph.addEdgeToNodes(node1, node2, 'left', 'right', src, dst, tokenValues, pRates, cRates, resnr, argnr, color)
                else:
                    if nodePoints[node1][0] > self.centerOfGraph.x():
                        self.graph.addEdgeToNodes(node1, node2, 'right', 'right', src, dst, tokenValues, pRates, cRates, resnr, argnr, color)
                    else:
                        self.graph.addEdgeToNodes(node1, node2, 'left', 'left', src, dst, tokenValues, pRates, cRates, resnr, argnr, color)


    def editTokens(self, src, dst, newTokens):
        self.graphData[src][dst]['tkns'] = newTokens
        newTokens = str(newTokens)
        self.graphData.updateTokens((src, dst), newTokens)

        #Also store the state after the change (Makes it more visual and makes it possible to step back to)
        self.graphData._storestate()
        
    def editNodeFunction(self, nodeName, newFunction):
        self.graphData.node[nodeName]['funcstr'] = newFunction
        self.graphData.updateNodeFunction(nodeName, newFunction)

    def editClashCode(self, nodeName, newClashCode):
        self.graphData.node[nodeName]['clashcode'] = newClashCode
        self.graphData.updateClashCode(nodeName, newClashCode)
    
    def editPRates(self, src, dst, newPRates):
        self.graphData[src][dst]['prates'] = newPRates
        newPRates = str(newPRates)
        self.graphData.updatePRates((src, dst), newPRates)

    def editCRates(self, src, dst, newCRates):
        self.graphData[src][dst]['crates'] = newCRates
        newCRates = str(newCRates)
        self.graphData.updateCRates((src, dst), newCRates)

    def getFireCount(self, src_dst, node):
        return self.graphData.node[src_dst]['firecount']

    def resetView(self):
        self.zoomLevel = 250
        self.setupMatrix()
        self.graphicsView.ensureVisible(QRectF(0,0,0,0))

    def setupMatrix(self):
        scale = 2.0 ** ((self.zoomLevel - 250) / 50.0)

        transform = QTransform()
        transform.scale(scale, scale)

        self.graphicsView.setTransform(transform)

    def zoomIn(self):
        self.zoomLevel += 10
        if self.zoomLevel > 350:
            self.zoomLevel = 350
        self.setupMatrix()

    def zoomOut(self):
        self.zoomLevel -= 10
        if self.zoomLevel < 0:
            self.zoomLevel = 0
        self.setupMatrix()    
