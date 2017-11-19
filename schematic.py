#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: Rinse Wester(r.wester@utwente.nl)

import networkx as nx
import json
import string
from collections import OrderedDict


class Schematic(nx.MultiDiGraph):
    """
    Class for modeling schematics.

    TODO: check if component already  exists and allow for multiple 
       connections between the same two components but on different sockets
    """

    def __init__(self):
        super().__init__()

        # other init code for the schematics 

    def add_link(self, src, dst, srcoutp, dstinp, name=''):
        """
        Add a link to the schematic.

        To prevent inconsistencies later on, first add nodes to the graph before
        adding edges.

        Parameters
        ----------
        src : source component
        dst : destination component
        srcoutp : name of output of source component
        dstinp : name of input of destination component
        """
        if src not in self.nodes():
            raise ValueError('No source component named ' + src + ' in schematic')

        if dst not in self.nodes():
            raise ValueError('No source component named ' + dst + ' in schematic')

        if srcoutp not in (self.node[src]['leftsockets'] + self.node[src]['rightsockets']):
            raise ValueError('No socket named ' + srcoutp + ' for source node ' + src)

        if dstinp not in (self.node[dst]['leftsockets'] + self.node[dst]['rightsockets']):
            raise ValueError('No socket named ' + dstinp + ' for destination node ' + dst)

        if name == '':
            linkName = "{}.{}>{}.{}".format(src, srcoutp, dst, dstinp)
        else:
            linkName = name

        super().add_edge(src, dst, srcoutp=srcoutp, dstinp=dstinp, name=linkName)


    def add_component(self, name, leftsockets=[], rightsockets=[], pos=(0,0)):
        """
        Add a component to the schematic.

        When constructing a graph, first add components using this method before
        adding links.

        Parameters
        ----------
        name : name of component
        leftsockets: list of names for sockets to which a link can be connected, shown on the left side of component
        rightsockets: similar to leftsockets except shown on the right side of component
        """
        super().add_node(name, leftsockets=leftsockets, rightsockets=rightsockets, pos=pos)

    def loadFromFile(self, filename):
        """
        Loads a schematic from a JSON file.

        Parameters
        ----------
        filename : string with file path

        Raises
        ------
        ValueError
            When the schematic is inconsistent as detected by the validate() method.
        """
        self.filename = filename
        with open(filename, 'r') as f:
            jsonstr = f.read()

        jsondata = json.loads(jsonstr)

        # Load all components and their attributes
        for jscomp in jsondata['components']:
            compName = jscomp['name']
            compPos = jscomp.get('pos', (0, 0))
            leftsockets = jscomp.get('leftsockets', [])
            rightsockets = jscomp.get('rightsockets', [])
            self.add_component(compName, leftsockets=leftsockets, rightsockets=rightsockets, pos=compPos)

        # Load all links and their attributes
        # TODO: add thickness property
        for jslink in jsondata['links']:
            sourceComp, sourceSocket = jslink['src'].split('.')
            destinationComp, destinationSocket = jslink['dst'].split('.')
            self.add_link(sourceComp, destinationComp, sourceSocket, destinationSocket)

        # Now that the schematic is construcuted, validate it:
        self.validate()
            
    def storeToFile(self, filename=''):
        """
        Stores the current schematic in a JSON file.

        Parameters
        ----------
        filename : string with filepath
            filename is an optional argument containing the file in which schematic is stored.
            When this argument is not used, the schematic is stored in the file from which it
            was initially read.
        """
        if filename == '':
            # no file name given so use file from which this schematic is made
            fname = self.filename
        else:
            fname = filename

        # Put all info into a temporary dict which will be transformed into a json string
        graphDict = OrderedDict({})
        
        # Store all the component of schematic in the temporary dict
        components = []
        for compName, compattr in self.nodes(data=True):
            compdict = OrderedDict({})
            compdict['name'] = compName
            compdict['pos'] = compattr['pos']
            if compattr['leftsockets'] != []:
                compdict['leftsockets'] = compattr['leftsockets']
            if compattr['rightsockets'] != []:
                compdict['rightsockets'] = compattr['rightsockets']
            components.append(compdict)

        # add all components to temporary dict in form of a list
        graphDict['components'] = components

        # Store all the edges of the graph in the temporary dict
        linkList = []
        for srcname, dstname, connattr in self.edges(data=True):
            linkdict = OrderedDict({})
            linkdict['src'] = srcname + '.' + connattr['srcoutp']
            linkdict['dst'] = dstname + '.' + connattr['dstinp']
            linkList.append(linkdict)

        # add all edges to temporary dict in form of a list
        graphDict['links'] = linkList

        # Last but not leat, write the graph to the file
        with open(fname, 'w') as outfile:
            json.dump(graphDict, outfile, indent=4)

    def validate(self):
        """
        Validates the schematic:
        """
        print('Warning: schematic validate not yet implemented')

if __name__ == '__main__':
    schem = Schematic()
    schem.loadFromFile('schem1.json')
    print("\n Schema 1:")
    print(schem.nodes(data=True))
    print(schem.edges(data=True))
    print('nr of components:', len(schem))

    schem.storeToFile('schem3.json')

    schem3 = Schematic()
    schem3.loadFromFile('schem3.json')
    print("\n Schema 3:")
    print(schem.nodes(data=True))
    print(schem.edges(data=True))
    print('nr of components:', len(schem))
    schem3.storeToFile('schem4.json')

