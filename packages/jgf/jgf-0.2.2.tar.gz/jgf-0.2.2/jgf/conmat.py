import numpy as np
import jgf
from collections import OrderedDict
import numbers


def _check_symmetric(a, rtol=1e-05, atol=1e-08):
	return np.allclose(a, a.T, rtol=rtol, atol=atol)

def load(filename='',compressed=None, weight="weight", getExtraData=False, noneNumericValue=0):
	"""
	Loads a JGF(Z) – Json Graph Format (gZipped) – file and converts it
	to a connectivity matrix represented by a numpy array.
	
	Parameters
	----------
	filename : str or file handler
			Path to the file or a file handler to be used as input.
	compressed : bool
			If true, the input file will be interpreted as being compressed.
			If not provided, this will be guessed from the file extension.
			Use '.jgfz' for compressed files.
	weight: str
		Name of the weight property to be used as weights for the connectivity
		matrix. By default, attribute `weight` is used. If this attribute is
		`None` or not present in the network, the generated matrix will be binary.
	getExtraData: bool
		If true, this function returns not only the graph but a dictionaries of
		properties as well.
	noneNumericValue: obj
		Value to be used as placeholder for invalid or none values in edge properties.
	Returns
	----------
	out : list of np.array of dim=2
			List of matrices network objects.
			
	"""
	inputGraphs = jgf.load(filename,compressed=compressed)
	graphs = []
	extraDataList = []
	for inputGraph in inputGraphs:
		nodeCount = 0
		if("node-count" in inputGraph):
			nodeCount = inputGraph["node-count"]

		directed = False
		if("directed" in inputGraph):
			directed = inputGraph["directed"]

		matrix = np.zeros((nodeCount,nodeCount))
		edges = []
		if("edges" in inputGraph):
			edges = inputGraph["edges"]
		
		weights = None
		if("edge-properties" in inputGraph):
			if(weight in inputGraph["edge-properties"]):
				weightData = inputGraph["edge-properties"][weight];
				if(isinstance(weightData, dict)):
					weights = [weightData[i] if i in weightData else 0 for i in range(len(edges))]
				else:
					weights = weightData
			
		for edgeIndex,(fromIndex,toIndex) in enumerate(edges):
			if(weights):
				matrix[fromIndex][toIndex] = weights[edgeIndex]
				if(not directed):
					matrix[toIndex][fromIndex] = weights[edgeIndex]
			else:
				matrix[fromIndex][toIndex] = 1
				if(not directed):
					matrix[toIndex][fromIndex] = 1

		if(getExtraData):
			extraData = dict()
			if("label" in inputGraph):
				extraData["label"] = inputGraph["label"]
			
			extraData["directed"] = directed
			if("network-properties" in inputGraph):
				extraData["network-properties"] = dict()
				for key,value in inputGraph["network-properties"].items():
					extraData["network-properties"][key] = value
				
			if("node-properties" in inputGraph):
				extraData["node-properties"] = dict()
				for key,values in inputGraph["node-properties"].items():
					if(isinstance(values, dict)):
						nodeData = [None]*nodeCount
						for indexKey,value in values.items():
							nodeIndex = int(indexKey)
							if(nodeIndex<0 or nodeIndex>=nodeCount):
								raise ValueError("Found a node index out of bounds. %d is not in range [%d,%d) "%(nodeIndex,0,nodeCount))
							nodeData[nodeIndex] = value
						extraData["node-properties"][key]=nodeData
					else:
						extraData["node-properties"][key] = values
			
			if("edge-properties" in inputGraph):
				edgeProperties = dict()
				for key,values in inputGraph["edge-properties"].items():
					if(key==weight):
						continue
					edgeData = [[None]*nodeCount for _ in range(nodeCount)]
					isNumeric = True;
					if(isinstance(values, dict)):
						for indexKey,value in values.items():
							edgeIndex = int(indexKey)
							if(edgeIndex<0 or edgeIndex>=edgeCount):
								raise ValueError("Found an edge index out of bounds. %d is not in range [%d,%d) "%(edgeIndex,0,edgeCount))
							fromIndex,toIndex = edges[edgeIndex]
							edgeData[fromIndex][toIndex] = value
							if(not directed):
								edgeData[toIndex][fromIndex] = value
							if(not isinstance(value, numbers.Number)):
								isNumeric=False
					else:
						for edgeIndex,(fromIndex,toIndex) in enumerate(edges):
							edgeData[fromIndex][toIndex] = values[edgeIndex]
							if(not directed):
								edgeData[toIndex][fromIndex] = values[edgeIndex]
							for value in values:
								if(not isinstance(value, numbers.Number)):
									isNumeric=False
									break
					if(isNumeric):
						edgeData = [[noneNumericValue if value is None else value for value in edgeRow] for edgeRow in edgeData]
					edgeProperties[key] = edgeData
				if(len(edgeProperties)>0):
					extraData["edge-properties"] = edgeProperties
			extraDataList.append(extraData)
		graphs.append(matrix)
		if(getExtraData):
			return graphs,extraDataList
		else:
			return graphs 



def save(matrices, filename='', weight="weight", compressed=None, mantainAllEdges=False,
	label=None, directed=None,networkProperties=None, nodeProperties=None,
	edgeProperties=None):
	"""
	Writes a list matrices as networks to a JGF(Z) – Json Graph Format (gZipped) – file.
	
	Parameters
	----------
	graphs : list of numpy matrices or a single connectivity matrix object
			Connectivity matrix to be saved.
	filename : str or file handler
			Path to the file or a file handler to be used as output.
	compressed : bool
			If true, the input file will be interpreted as being compressed.
			If not provided, this will be guessed from the file extension.
			Use '.jgfz' for compressed files.
	mantainAllEdges : bool
	label : list or str
		Labels used for the networks in order. If a single value is provided, it will be
		replicated to all networks.
	directed : list or bool
		Set if the networks are directed or not. If a single value is provided, it will be
		replicated to all networks.
	networkProperties : list or dict
		Dictionary containing the network properties. If a single dictionary is provided, it
		will be replicated to all the networks.
	nodeProperties : list or dict
		Dictionary containing the node properties. If a single dictionary is provided, it
		will be replicated to all the networks. Each entry in the dictionaries must be arrays
		of properties indexed according to the order of columns/rows in the matrix.
	edgeProperties : list or bool
		Dictionary containing the edge properties. If a single dictionary is provided, it will be
		replicated to all the networks. Each entry must contain a matrix of values assigned to
		each edge (nodes pair).
	"""
	exportGraphs = []
	if(not isinstance(matrices,list)):
		matrices = [matrices]

	if(label is not None and not isinstance(label,list)):
		label = [label]*len(matrices);
	
	if(directed is not None and not isinstance(directed,list)):
		directed = [directed]*len(matrices);

	if(networkProperties is not None and not isinstance(networkProperties,list)):
		networkProperties = [networkProperties]*len(matrices);
	
	if(nodeProperties is not None and not isinstance(nodeProperties,list)):
		nodeProperties = [nodeProperties]*len(matrices);
	
	if(edgeProperties is not None and not isinstance(edgeProperties,list)):
		edgeProperties = [edgeProperties]*len(matrices);
	
	for matrixIndex, matrix in enumerate(matrices):
		exportGraph = OrderedDict()
		
		nodeCount = len(matrix)
		adjacencyMatrix = np.array(matrix)
		if(directed is not None and len(directed)>matrixIndex):
			networkDirected = directed[matrixIndex]
		else:
			networkDirected = not _check_symmetric(adjacencyMatrix)
		
		if(networkDirected):
			if(not mantainAllEdges):
				edges = [(f,t) for f in range(nodeCount) for t in range(nodeCount) if adjacencyMatrix[f][t]!=0]
			else:
				edges = [(f,t) for f in range(nodeCount) for t in range(nodeCount)]
		else:
			if(not mantainAllEdges):
				edges = [(f,t) for f in range(nodeCount) for t in range(f,nodeCount) if adjacencyMatrix[f][t]!=0]
			else:
				edges = [(f,t) for f in range(nodeCount) for t in range(f,nodeCount)]
			#tuple(zip(*

		edgeIndices = tuple(zip(*edges));
		
		

		if(label is not None and len(label)>matrixIndex):
			exportGraph["label"] = label[matrixIndex]

		exportGraph["node-count"] = nodeCount
		exportGraph["directed"] = networkDirected

		if(networkProperties is not None and len(networkProperties)>matrixIndex):
			if(len(networkProperties[matrixIndex])>0):
				exportGraph["network-properties"] = networkProperties[matrixIndex]
		
		
		exportGraph["edges"] = edges


		if(nodeProperties is not None and len(nodeProperties)>matrixIndex):
			if(len(nodeProperties[matrixIndex])>0):
				exportGraph["node-properties"] = OrderedDict(nodeProperties[matrixIndex])
		
		if(edgeProperties is not None and len(edgeProperties)>matrixIndex):
			exportEdgeProperties = OrderedDict()
			for key,values in edgeProperties[matrixIndex].items():
				valuesArray = np.array(values)
				if(valuesArray.shape[0] == nodeCount and valuesArray.shape[1] == nodeCount):
					propertyData = valuesArray[edgeIndices]
					exportEdgeProperties[key] = propertyData
				exportGraph["edge-properties"] = OrderedDict(exportEdgeProperties)
		
		if(weight is not None):
			weights = adjacencyMatrix[edgeIndices]
			if("edge-properties" not in exportGraph):
				exportGraph["edge-properties"] = OrderedDict()
			exportGraph["edge-properties"][weight] = weights
		exportGraphs.append(exportGraph)
	jgf.save(exportGraphs,filename,compressed)
