
import io
import re
import sys

import numpy as np
import json
import gzip
import os.path
import warnings
from collections import OrderedDict

import numpy as np

class NumpyEncoder(json.JSONEncoder):
	""" Custom encoder for numpy data types """
	def default(self, obj):
		if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
												np.int16, np.int32, np.int64, np.uint8,
												np.uint16, np.uint32, np.uint64)):

			return int(obj)

		elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
			return float(obj)

		elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
			return {'real': obj.real, 'imag': obj.imag}

		elif isinstance(obj, (np.ndarray,)):
			return obj.tolist()

		elif isinstance(obj, (np.bool_)):
			return bool(obj)

		elif isinstance(obj, (np.void)): 
			return None

		return json.JSONEncoder.default(self, obj)

class JGFParseError(Exception):
	pass

class JGFParseWarning(UserWarning):
	pass

_nonMetaNodeAttributes = set(["type","label","metadata"])
_nonMetaEdgeAttributes = set(["type","label","directed","relation","metadata"])
_nonMetaGraphAttributes = set(["id","type","label","metadata"])

def _JGFAddNodeAttribute(graph,key,values):
	isDictionary = isinstance(values,dict) ;
	if("nodes" in graph and (isDictionary or len(values)==len(graph["nodes"]))):
		if(isDictionary):
			indices = values.keys()
		else:
			indices = range(len(values))
		jsonNodes = graph["nodes"]
		if(key in _nonMetaNodeAttributes):
				for nodeIndex in indices:
					jsonNodes[str(nodeIndex)][key] = values[nodeIndex]
		else:
			for nodeIndex in indices:
				nodeEntry = jsonNodes[str(nodeIndex)]
				if ("metadata" not in nodeEntry):
					nodeEntry["metadata"] = OrderedDict()
				nodeEntry["metadata"][key] = values[nodeIndex]
	else:
		raise ValueError("Node properties must have same length as node-count.")


def _JGFAddEdgeAttribute(graph,key,values):
	isDictionary = isinstance(values,dict) ;
	if("edges" in graph and (isDictionary or len(values)==len(graph["edges"]))):
		if(isinstance(values,dict)):
			indices = values.keys()
		else:
			indices = range(len(values))
		jsonEdges = graph["edges"]
		if(key in _nonMetaEdgeAttributes):
			for edgeIndex in indices:
				jsonEdges[str(edgeIndex)][key] = values[edgeIndex]
		else:
			for edgeIndex in range(len(values)):
				edgeEntry = jsonEdges[edgeIndex]
				if ("metadata" not in edgeEntry):
					edgeEntry["metadata"] = OrderedDict()
				edgeEntry["metadata"][key] = values[edgeIndex]
	else:
		raise ValueError("Edge properties must have same length as edges.")



def _JGFAddGraphAttribute(graph,key,value):
	if(key in _nonMetaGraphAttributes):
		graph[key] = value
	else:
		if ("metadata" not in graph):
			graph["metadata"] = OrderedDict()
		graph["metadata"][key] = value


def _convertToJGFEntry(graph):
	graphJSON = OrderedDict()

	if("label" in graph):
		_JGFAddGraphAttribute(graphJSON,"label",graph["label"]);
	if("directed" in graph):
		graphJSON["directed"] = graph["directed"]
	if("network-properties" in graph):
		networkProperties = graph["network-properties"]
		for key,value in networkProperties.items():
			_JGFAddGraphAttribute(graphJSON,key,value)

	if("node-count" in graph and graph["node-count"]>0):
		nodeCount = graph["node-count"]
		graphJSON["nodes"] = OrderedDict((str(nodeIndex),OrderedDict()) for nodeIndex in range(nodeCount))
	else:
		raise ValueError("graph must contain node-count property")
	if("edges" in graph and len(graph["edges"])>0):
		graphJSON["edges"] = [{"source":str(fromNodeIndex),"target":str(toNodeIndex)} for edgeIndex,(fromNodeIndex,toNodeIndex) in enumerate(graph["edges"])]

	if("node-properties" in graph):
		nodeProperties = graph["node-properties"]
		for key,values in nodeProperties.items():
			_JGFAddNodeAttribute(graphJSON,key,values)
	if("edge-properties" in graph):
		edgeProperties = graph["edge-properties"]
		for key,values in edgeProperties.items():
			_JGFAddEdgeAttribute(graphJSON,key,values)
	return graphJSON


def _convertFromJGFEntry(graphJSON):
	graph = OrderedDict()
	hasNodes = "nodes" in graphJSON
	hasEdges = "edges" in graphJSON

	if(not hasNodes and hasEdges):
		raise JGFParseError("JGF files must contain 'nodes' if 'edges' is defined.")

	directed = False
	if("directed" in graphJSON):
		directed = graphJSON["directed"]
	else:
		warnings.warn("'directed' was not found in the JGF file. This parser only works for fully directed/undirected networks. The whole network is now considered undirected.", JGFParseWarning)


	graphProperties = OrderedDict()
	if("label" in graphJSON): # root graph property
		graph["label"] = graphJSON["label"]
	if("id" in graphJSON):
		graphProperties["id"] = graphJSON["id"]
	if("type" in graphJSON):
		graphProperties["type"] = graphJSON["type"]

	graph["directed"] = directed

	if(hasNodes):
		graph["node-count"] = len(graphJSON["nodes"])
		
	if("metadata" in graphJSON):
		for key, value in graphJSON["metadata"].items():
			graphProperties[key] = value

	if(len(graphProperties)>0):
		graph["network-properties"] = graphProperties

	nodeProperties = OrderedDict()
	nodeIDToIndex = OrderedDict()
	nodeIndexToID = []
	digitIndices = True
	if(hasNodes):
		for nodeID, nodeData in graphJSON["nodes"].items():
			if(nodeID not in nodeIDToIndex):
				nodeIDToIndex[nodeID] = len(nodeIndexToID)
				nodeIndexToID.append(nodeID)
				if(not nodeID.isdigit()):
					digitIndices = False
			for key,value in nodeData.items():
				if(key!="metadata"):
					if(key not in nodeProperties):
						nodeProperties[key] = OrderedDict()
					nodeProperties[key][nodeID] = value
			
			if("metadata" in nodeData):
				for key,value in nodeData["metadata"].items():
					if(key not in nodeProperties):
						nodeProperties[key] = OrderedDict()
					nodeProperties[key][nodeID] = value
		contiguosIndices = False
		if(digitIndices):
			IDs = [int(ID) for ID in nodeIndexToID]
			if(max(IDs)==len(IDs) and min(IDs) == 0):
				contiguosIndices = True #No need for IDs
				nodeIDToIndex = [str(ID) for ID in range(len(IDs))]
				nodeIndexToID = OrderedDict((str(ID),ID) for ID in range(len(IDs)))
		for key in nodeProperties:
			if(len(nodeProperties[key]) == len(nodeIDToIndex)):
				#all nodes have property so convert it to an array
				nodeProperties[key] = [nodeProperties[key][ID] for ID in nodeIDToIndex]
			else:
				#some nodes do not have this property, so reindex the dictionary
				nodeProperties[key] = OrderedDict((nodeIDToIndex[ID],value) for ID,value in nodeProperties[key].items())
		if(contiguosIndices):
				nodeProperties["ID"] = nodeIndexToID
	
	edges = []
	edgeProperties = OrderedDict()
	if(hasEdges):
		for edgeIndex, edgeData in enumerate(graphJSON["edges"]):
			hasSource = "source" in edgeData
			hasTarget = "target" in edgeData
			if(not hasSource or not hasTarget):
				raise JGFParseError("Edges must contain both source and target attributes.")
			
			sourceID = edgeData["source"]
			targetID = edgeData["target"]

			if(sourceID not in nodeIDToIndex or targetID not in nodeIDToIndex):
				raise JGFParseError("Node %s is not present in the list of nodes. The file was not loaded."%sourceID)
			
			sourceIndex = nodeIDToIndex[sourceID]
			targetIndex = nodeIDToIndex[targetID]
			edges.append((sourceIndex,targetIndex))

			for key,value in edgeData.items():
				if(key!="metadata" and key!="source" and key!="target"):
					if(key not in edgeProperties):
						edgeProperties[key] = OrderedDict()
					edgeProperties[key][edgeIndex] = value
			
			if("metadata" in edgeData):
				for key,value in edgeData["metadata"].items():
					if(key not in edgeProperties):
						edgeProperties[key] = OrderedDict()
					edgeProperties[key][edgeIndex] = value
		
		for key in edgeProperties:
			if(len(edgeProperties[key]) == len(edges)):
				#all nodes have property so convert it to an array
				edgeProperties[key] = [edgeProperties[key][ID] for ID in edgeProperties[key]]
			else:
				#some nodes do not have this property, so reindex it
				edgeProperties[key] = OrderedDict((ID,value) for ID,value in edgeProperties[key].items())

	if(len(edges)>0):
		graph["edges"] = edges
	if(len(nodeProperties)>0):
		graph["node-properties"] = nodeProperties
	if(len(edgeProperties)>0):
		graph["edge-properties"] = edgeProperties
	return graph



def load(filename='',compressed=None):
	"""
	Loads a JGF(Z) – Json Graph Format (gZipped) – file and converts it
	to a list of JXNF – Json compleX Network Format – dictionaries.
	
	Parameters
	----------
	filename : str or file handle
			Path to the file or a file handle to be used as input.
	compressed : bool
			If true, the input file will be interpreted as being compressed.
			If not provided, this will be guessed from the file extension.
			Use '.jgfz' for compressed files.

	Returns
	-------
	out : List of OrderedDict
			Data readed from the JGF(Z) file formatted as a list of JXNF
			dictionaries.
	"""
	shallCleanupHandler = False;
	if(isinstance(filename, str)):
		shallCleanupHandler = True
		if(compressed is None):
			fileExtension = os.path.splitext(filename)[1]
			if(fileExtension==".jgfz"):
				compressed = True
			else:
				compressed = False
		if(compressed):
			filehandler = gzip.open(filename,"rt")
		else:
			filehandler = open(filename,"rt")
	else:
		shallCleanupHandler=False
		if(compressed is None):
			compressed = False
		filehandler = filename

	importJSON = json.load(filehandler,object_pairs_hook=OrderedDict)
	if("graph" in importJSON):
		graphJSONArray = [importJSON["graph"]]
	elif("graphs" in importJSON):
		graphJSONArray = importJSON["graphs"]
	else:
		graphJSONArray = []
	graphs = [_convertFromJGFEntry(graphJSON) for graphJSON in graphJSONArray]
	if(shallCleanupHandler):
		filehandler.close()
	return graphs


	



def save(graphs,filename="",compressed=None):
	"""
	Writes a list of JXNF – Json compleX Network Format – dictionaries to 
	a JGF(Z) – Json Graph Format (gZipped) – file.
	
	Parameters
	----------
	graphs : list of dict
			List of dictionaries in JXNF.
	filename : str or file handle
			Path to the file or a file handle to be used as output.
	compressed : bool
			If true, the input file will be interpreted as being compressed.
			If not provided, this will be guessed from the file extension.
			Use '.jgfz' for compressed files.
	"""
	
	shallCleanupHandler = False;
	if(isinstance(filename, str)):
		shallCleanupHandler = True
		if(compressed is None):
			fileExtension = os.path.splitext(filename)[1]
			if(fileExtension==".jgfz"):
				compressed = True
			else:
				compressed = False
		if(compressed):
			filehandler = gzip.open(filename,"wt")
		else:
			filehandler = open(filename,"wt")
	else:
		shallCleanupHandler=False
		if(compressed is None):
			compressed = False
		filehandler = filename

	if(not isinstance(graphs, list)):
		if(isinstance(graphs, dict)):
			graphs = [graphs]
		else:
			raise TypeError(f"Argument graphs must be of type dict or a list of dicts, not {type(graphs)}")

	exportGraphs = []
	for graph in graphs:
		exportGraphs.append(_convertToJGFEntry(graph))
	
	exportJSON={}
	if(len(graphs)==1):
		exportJSON["graph"] = exportGraphs[0]
	else:
		exportJSON["graphs"] = exportGraphs
	
	json.dump(exportJSON,filehandler,cls=NumpyEncoder)
	if(shallCleanupHandler):
		filehandler.close()

