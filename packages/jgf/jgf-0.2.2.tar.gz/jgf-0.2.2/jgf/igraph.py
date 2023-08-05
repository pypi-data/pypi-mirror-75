import numpy as np
import jgf
from collections import OrderedDict

def load(filename='',compressed=None):
	"""
	Loads a JGF(Z) – Json Graph Format (gZipped) – file and converts it
	to an igraph.Graph object.
	
	Parameters
	----------
	filename : str or file handle
			Path to the file or a file handle to be used as input.
	compressed : bool
			If true, the input file will be interpreted as being compressed.
			If not provided, this will be guessed from the file extension.
			Use '.jgfz' for compressed files.

	Returns
	----------
	out : list of igraph.Graph
			List of igraph network objects.
	"""

	import igraph as ig
	inputGraphs = jgf.load(filename,compressed=compressed)
	graphs = []
	for inputGraph in inputGraphs:
		nodeCount = 0
		if("node-count" in inputGraph):
			nodeCount = inputGraph["node-count"]

		directed = False
		if("directed" in inputGraph):
			directed = inputGraph["directed"]

		edges = []
		edgeCount = 0
		if("edges" in inputGraph):
			edges = inputGraph["edges"]
			edgeCount = len(edges)

		graph = ig.Graph(nodeCount,directed=directed,edges=edges)
		if("label") in inputGraph:
			graph["label"] = inputGraph["label"]
		
		if("network-properties" in inputGraph):
			for key,value in inputGraph["network-properties"].items():
				graph[key] = value
			
		if("node-properties" in inputGraph):
			for key,values in inputGraph["node-properties"].items():
				if(isinstance(values, dict)):
					for indexKey,value in values.items():
						nodeIndex = int(indexKey)
						if(nodeIndex<0 or nodeIndex>=nodeCount):
							raise ValueError("Found a node index out of bounds. %d is not in range [%d,%d) "%(nodeIndex,0,nodeCount))
						graph.vs[nodeIndex][key] = values[indexKey]
				else:
					graph.vs[key] = values
		
		if("edge-properties" in inputGraph):
			for key,values in inputGraph["edge-properties"].items():
				if(isinstance(values, dict)):
					for indexKey,value in values.items():
						edgeIndex = int(indexKey)
						if(edgeIndex<0 or edgeIndex>=edgeCount):
							raise ValueError("Found an edge index out of bounds. %d is not in range [%d,%d) "%(edgeIndex,0,edgeCount))
						graph.es[edgeIndex] = values[indexKey]
				else:
					graph.es[key] = values
		
		graphs.append(graph)
	return graphs 
		


def save(graphs, filename='',compressed=None):
	"""
	Writes a list igraph.Graph networks to a JGF(Z) – Json Graph Format (gZipped) – file.
	
	Parameters
	----------
	graphs : list of igraph.Graph objects or a single Graph object
			Graphs to be saved.
	filename : str or file handle
			Path to the file or a file handle to be used as output.
	compressed : bool
			If true, the input file will be interpreted as being compressed.
			If not provided, this will be guessed from the file extension.
			Use '.jgfz' for compressed files.
	"""

	import igraph as ig
	exportGraphs = []
	if(not isinstance(graphs,list)):
		graphs = [graphs]
	
	for graph in graphs:
		exportGraph = OrderedDict()
		if("label" in graph.attributes()):
			exportGraph["label"] = graph["label"]

		exportGraph["node-count"] = graph.vcount()
		exportGraph["directed"] = graph.is_directed() 

		networkProperties = OrderedDict()
		for key in graph.attributes():
			if(key!="label"):
				networkProperties[key] = graph[key]
		if(len(networkProperties)>0):
			exportGraph["network-properties"] = networkProperties
		
		exportGraph["edges"] = graph.get_edgelist()

		nodeProperties = OrderedDict()
		for key in graph.vertex_attributes():
			values = graph.vs[key]
			foundNone = False
			for value in values:
				if(value is None):
					foundNone=True
					break
			if(foundNone):
				nodeProperties[key] = OrderedDict((index,value) for index,value in enumerate(values) if value is not None)
			else:
				nodeProperties[key] = values
		if(len(nodeProperties)>0):
			exportGraph["node-properties"] = nodeProperties
		
		edgeProperties = OrderedDict()
		for key in graph.edge_attributes():
			values = graph.es[key]
			foundNone = False
			for value in values:
				if(value is None):
					foundNone=True
					break
			if(foundNone):
				edgeProperties[key] = OrderedDict((index,value) for index,value in enumerate(values) if value is not None)
			else:
				edgeProperties[key] = values
		if(len(edgeProperties)>0):
			exportGraph["edge-properties"] = edgeProperties
		exportGraphs.append(exportGraph)
	jgf.save(exportGraphs,filename,compressed)



