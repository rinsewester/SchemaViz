#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Widget to display simulation data of a CSDF graph.

author: Sander Giesselink

"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from node import Node
from edge import Edge

class Graph(QWidget):

    def __init__(self, graphWidget, scene, view):
        super().__init__()

        self.graphWidget = graphWidget
        self.scene = scene
        self.view = view
      
        self.edgeList = []
        self.nodeList = []

    def clearGraph(self):
        #Delete all items from the scene and clear lists
        for i in range(len(self.nodeList)):
            self.scene.removeItem(self.nodeList[i])

        for i in range(len(self.edgeList)):
            self.scene.removeItem(self.edgeList[i])

        self.nodeList.clear()
        self.edgeList.clear()
            
    def addNode(self, name, x, y):
        newNode = Node(self, self.view, name)
        newNode.setPos(x, y)
        newNode.setZValue(0)
        
        #Add node to the scene and list
        self.scene.addItem(newNode)
        self.nodeList.append(newNode)

    def addEdge(self, beginPoint, endPoint, beginSide, endSide, edgeSelfLoops, src, dst, pRates, cRates):
        newEdge = Edge(beginPoint, endPoint, beginSide, endSide, edgeSelfLoops, pRates, cRates)

        #Place edges always behind nodes
        newEdge.setZValue(1)
        
        #Add edge to the scene and list
        self.scene.addItem(newEdge)
        self.edgeList.append(newEdge)

        return newEdge

    def addEdgeToNodes(self, beginNodeIndex, endNodeIndex, beginSide, endSide, src = '', dst = '', pRates = [0], cRates = [0], resnr = '', argnr = ''):
        beginNode = self.nodeList[beginNodeIndex]
        endNode = self.nodeList[endNodeIndex]
        
        #Get points on the nodes that the edge can connect to
        beginPoint = beginNode.getIOPointForEdge(beginSide, 2)
        endPoint = endNode.getIOPointForEdge(endSide, 1)

        #Set the beginNode as an output
        beginNode.setIOType(beginSide, 2, resnr)
        #Set the endNode as an input
        endNode.setIOType(endSide, 1, argnr)

        #Add new IO ports to nodes for future edges
        beginNode.addNewIO(beginSide, 0)
        endNode.addNewIO(endSide, 0)
        
        #Create edge between the 2 nodes
        edge = self.addEdge(beginPoint, endPoint, beginSide, endSide, beginNode == endNode, src, dst, pRates, cRates)

        #Give both nodes a reference to the created edge
        beginNode.addEdge(edge, 'begin')
        endNode.addEdge(edge, 'end')


    def editNodeFunction(self, name, newFunction):
        self.graphWidget.editNodeFunction(name, newFunction)

    def editClashCode(self, name, newClashCode):
        self.graphWidget.editClashCode(name, newClashCode)
    
    def editPRates(self, src, dst, newPRates):
        self.graphWidget.editPRates(src, dst, newPRates)

    def editCRates(self, src, dst, newCRates):
        self.graphWidget.editCRates(src, dst, newCRates)

    def getFireCount(self, src_dst, node):
        return self.graphWidget.getFireCount(src_dst, node)