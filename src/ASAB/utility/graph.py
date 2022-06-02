## Get the configuration
try:
    # if there is a main file, get conf from there
    from __main__ import conf   # https://stackoverflow.com/questions/6011371/python-how-can-i-use-variable-from-main-file-in-module
except ImportError:
    # if the import was not successful, go to default config
    from ASAB.configuration import default_config
    conf = default_config.config

## Imports from ASAB
from ASAB.utility.helpers import saveToFile
from ASAB.driver.CetoniDevice_driver import getValvePositionDict

## Other imports
from typing import Union
import networkx as nx   # https://networkx.org/documentation/stable/tutorial.html
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def loadGraph(path_to_graphDict:str=conf["CetoniDeviceDriver"]["setup"]):
    ''' This function loads a graph and the corresponding positions to allow for drawing of the graph. '''
    # Check the type of the input
    if not isinstance(path_to_graphDict, str):  # https://pytutorial.com/python-check-variable-type#isinstance()-built-in-function
        raise ValueError
    # Open and read the file containing the data
    with open(path_to_graphDict, "r", encoding="utf-8") as file:
        rawString = file.read()
    # Make the rawString string to a dict
    this_graph = eval(rawString)
    graph = nx.DiGraph(this_graph)
    # Do the same for the positions
    with open(f"{str(path_to_graphDict[0:-4])}_positions.txt", "r", encoding="utf-8") as file2:
        rawString = file2.read()
    # Make the rawString string to a dict
    positions = eval(rawString)
    return graph

def getGraph(graph:Union[str,dict,nx.classes.digraph.DiGraph]):
    ''' This function does a type check of the given graph and if it is not yet a graph object, it loads a graph object from the given file. '''
    if isinstance(graph, nx.classes.digraph.DiGraph):
        graph = graph
    elif isinstance(graph, str):
        graph = loadGraph(graph)
    elif isinstance(graph, dict):
        graph = nx.DiGraph(graph)
    else:
        print("graph:", type(graph))
        raise ValueError(f'Incorrect type of {graph} {type(graph)} instead of str, dict or nx.classes.digraph.DiGraph.')
    return graph

def findClosest(node:str, candidates:list, graph:Union[str,nx.classes.digraph.DiGraph]=conf["CetoniDeviceDriver"]["setup"], valvePositionDict:Union[str,dict]=conf["CetoniDeviceDriver"]["valvePositionDict"], weight:str="dead_volume", direction:str="out"):
    ''' Finds the closest candidate to a given node regarding a specified weight for the path. The direction of the search can be either
    incoming to the node or outgoing from the node. The default is outgoing. The function returns the closest node among the given candidates
    and the path from the specified node to this candidate node. candidates is of type "list". '''
    ## Check the input types
    # check node, candidates, weight and direction
    # if (not isinstance(node, str)) or (not isinstance(candidates, list)) or (not isinstance(weight, str)) or (not isinstance(direction, str)):
    #     raise ValueError
    # check graph
    graph = getGraph(graph)
    # check valvePositionDict
    valvePositionDict = getValvePositionDict(valvePositionDict)
    # Put together a dataframe to store the path lengths
    startingData = np.zeros((len(candidates), 3), dtype=object)
    startingData[:,0] = candidates
    shortest_distances = pd.DataFrame(startingData, columns=["candidate", "shortestPathLength", "shortestPath"], dtype=object)
    # Calculate for each candidate the shortest path with respect to the given weight
    for candidate in candidates:
        # If the direction is outgoing from the node, check the paths starting from the node and ending in the candidate
        if direction=="out":
            try:
                # Get a valid path
                path_out = findPath(start_node=node, end_node=candidate, valvePositionDict=valvePositionDict, graph=graph, weight=weight)
                # Get the total weight of the path
                length_out = getTotalQuantity(nodelist=path_out, quantity=weight)
                # Store the values in the prepared dataframe
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPathLength"] = length_out
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPath"] = str(path_out)
            except (IndexError, nx.exception.NetworkXNoPath):   # https://stackoverflow.com/questions/6095717/python-one-try-multiple-except
                # Store infinite length and the string 'no path' in the prepared dataframe
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPathLength"] = np.inf
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPath"] = 'no path'
        # If the direction is incoming to the node, check the paths starting from the candidate and ending in the node
        elif direction=="in":
            try:
                # Get a valid path
                path_in = findPath(start_node=candidate, end_node=node, valvePositionDict=valvePositionDict, graph=graph, weight=weight)
                # Get the total weight of the path
                length_in = getTotalQuantity(nodelist=path_in, quantity=weight)
                # Store the values in the prepared dataframe
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPathLength"] = length_in
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPath"] = str(path_in)
            except (IndexError, nx.exception.NetworkXNoPath):   # https://stackoverflow.com/questions/6095717/python-one-try-multiple-except
                # Store infinite length and the string 'no path' in the prepared dataframe
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPathLength"] = np.inf
                shortest_distances.loc[shortest_distances["candidate"]==candidate, "shortestPath"] = 'no path'

    # Find the closest candidate in the dataframe
    closest = shortest_distances.loc[shortest_distances["shortestPathLength"]==min(shortest_distances["shortestPathLength"]), "candidate"].values[0]
    # Extract the path to the closest candidate from the dataframe
    pathToClosest = eval(shortest_distances.loc[shortest_distances["candidate"]==closest, "shortestPath"].values[0])
    return closest, pathToClosest

def findPathAB(start_node:str, end_node:str, valvePositionDict:Union[str,dict]=conf["CetoniDeviceDriver"]["valvePositionDict"], graph:Union[str,nx.DiGraph]=conf["CetoniDeviceDriver"]["setup"], weight:str="dead_volume"):
    ''' This function finds a path in the graph representing the setup. It uses the function "pathIsValid" to makes sure that no more than two nodes belonging to the same valve are included
    in the path. If this condition is not met by the suggestion obtained by the Dijkstra algorithm, it removes connections in a copy of the graph until it finds a valid path. The path is searched
    from start_node to end_node. ''' # TODO: Add optional nodes in between and conditions for the path other than just minimal weight.
    ## Check the input types
    # check start_node, end_node, weight and direction
    if (not isinstance(start_node, str)) or (not isinstance(end_node, str)) or (not isinstance(weight, str)):
        raise ValueError
    # check graph
    graph = getGraph(graph)
    # check valvePositionDict
    valvePositionDict = getValvePositionDict(valvePositionDict)
    # Find the initial path using the Dijkstra-algorithm.
    initial_path = nx.dijkstra_path(graph, start_node, end_node, weight=weight)
    # Get the valves for the nodes in the path
    valveList_orig = [getValveFromName(node, valvePositionDict) for node in initial_path]
    # Transfer the path to a pandas dataframe
    valveList = pd.DataFrame(valveList_orig)
    # Drop the NaN values originating from nodes not belonging to valves
    valveList = valveList.dropna()
    # Get number of occurences of each valve in valveList
    occurance = valveList.value_counts()    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html
    if pathIsValid(initial_path, valvePositionDict):
        # If the initial path is valid, return the path
        return initial_path
    else:
        # Transfer the initial path to a numpy array
        path = np.array(initial_path)
        # Generate an empty dataframe for the candidates for alternative paths
        candidate_graphs = pd.DataFrame(columns=["removed_edge", "new_graph", "new_path", "total_weight", "validity", "valveCount"])
        # Go through all entries in the occurance
        for occ in occurance:
            # If the occurance exceeds 2, meaning that one valve is contained more than two times in the graph
            if occ > 2:
                # For every occurance above 2, get the valve
                valves = occurance[occurance.values==occ].index
                for valv in valves:
                    # Get the index, where the original valve list has the valve
                    idx =  np.where(np.array(valveList_orig)==valv[0])
                    # Get the node at these indices in the path
                    nodeOcc = path[idx]
                    for j in range(len(nodeOcc)-1):
                        # For the the nodes identified in the path, copy the graph
                        new_graph = graph.copy()
                        # Remove one edge from the copied graph between the selected node and its subsequent node
                        new_graph.remove_edge(nodeOcc[j], nodeOcc[j+1])
                        # Save the start and end node of the removed edge
                        removed_edge = (nodeOcc[j], nodeOcc[j+1])
                        try:    # https://stackoverflow.com/questions/26059424/on-error-resume-next-in-python
                            # Try to find an alternative path in the new graph using the Dijkstra algorithm and calculate the relevant measures
                            new_path = nx.dijkstra_path(new_graph, start_node, end_node, weight)
                            total_weight = getTotalQuantity(nodelist=new_path, quantity=weight)
                            validity = pathIsValid(path=new_path, valvePositionDict=valvePositionDict)
                            valvesNewPath = pd.DataFrame([getValveFromName(node_name=nod, valvePositionDict=valvePositionDict) for nod in new_path]).dropna()
                            valveCount = valvesNewPath.shape[0]
                        except: #KeyError: TODO: Be more specific on the Type of error!!!
                            # If an error occurs, assume that no path could be found and set the measures accordingly
                            new_path = "noPath"
                            total_weight = np.inf
                            validity = False
                            valveCount = np.inf
                        # Put the relevant measures in a dataframe and name its columns according to the candidate_graphs dataframe
                        candidate = pd.DataFrame(data=np.array([removed_edge, new_graph, new_path, total_weight, validity, valveCount], dtype=object)).transpose()
                        candidate.columns=["removed_edge", "new_graph", "new_path", "total_weight", "validity", "valveCount"]
                        # Add the new candidate to the candidate_graphs dataframe
                        candidate_graphs = pd.concat([candidate_graphs, candidate], axis=0, ignore_index=True)
        # Select the row in the dataframe, which contains a valid path.
        selection = candidate_graphs.loc[(candidate_graphs["validity"]==True)]
        # Among the valid paths select the one with minimum weight and subsequently the one with minimum valveCount.
        fineSelection = selection.loc[selection["total_weight"]==np.min(selection["total_weight"])]
        fineSelection = fineSelection.loc[selection["valveCount"]==np.min(selection["valveCount"])]
        # Get the path of one of the optimum valid paths
        selected_path = fineSelection.get("new_path").array[0]
        return selected_path

# TODO: Test this function
def findPath(start_node:str, end_node:str, via:list=[], valvePositionDict:Union[str,dict]=conf["CetoniDeviceDriver"]["valvePositionDict"], graph:Union[str,nx.DiGraph]=conf["CetoniDeviceDriver"]["setup"], weight:str="dead_volume"):
    ''' This function finds a path from the start node to the end node and if applicable passes the nodes given as a list in 'via' in the sequence given. '''
    ## If no additional nodes to pass are given, search for a path between start_node and end_node.
    # check, if no additional nodes are given
    if via == []:
        # call the function, which finds a path from start_node to end_node and return its result
        return findPathAB(start_node=start_node, end_node=end_node, valvePositionDict=valvePositionDict, graph=graph, weight=weight)
    else:
        ## If there are additional nodes, find a path to pass them all in the given order
        # add the start_node to the beginning of the list and the end_node to the end of the list
        nodesToPass = [start_node] + via + [end_node]
        # prepare a list to save the total path
        totalPath = []
        ## Find a path from each node in the list of nodes to pass to its successor and assemble the paths to the total path
        # iterate over all nodes that need to be passed
        for i in range((len(nodesToPass) - 1)):
            print(nodesToPass[i],nodesToPass[i+1])
            # get the path from this node to its successor
            path = findPathAB(start_node=nodesToPass[i], end_node=nodesToPass[i+1], valvePositionDict=valvePositionDict, graph=graph, weight=weight)
            # add this path to the total path omitting its end node
            totalPath.extend(path[:-1]) # https://stackoverflow.com/questions/252703/what-is-the-difference-between-pythons-list-methods-append-and-extend 
        # add the final end_node to the total Path, because it is omitted in the for-loop
        totalPath.append(end_node)
        ## Return the path, if it is valid
        if pathIsValid(totalPath):
            return totalPath
        # else raise a ValueError
        else:
            raise ValueError('No path is found, which passes all the nodes in the given order. Please check the requirements.')

# TODO: Add comments
def checkConsistency(path_nodes:str=conf["graph"]["pathNodes"], path_edges:str=conf["graph"]["pathEdges"], path_tubing:str=conf["graph"]["pathTubing"]):
    ''' This function checks, if the setup files for the graph are consistent. It checks whether all the edges given in
    tubing.csv are contained in edges.csv and if all nodes referenced in tubing.csv are contained in nodes.csv. It returns
    three results for edges and nodes, edges and nodes.  '''
    edges_frame = pd.read_csv(path_edges, sep=";")
    nodes_frame = pd.read_csv(path_nodes, sep=";")
    tubing_frame = pd.read_csv(path_tubing, sep=";")
    tubing_nodes_frame = pd.concat([tubing_frame["start"], tubing_frame["end"]], axis=0)
    tubing_edges_frame = tubing_frame["edge"]

    edges = list(edges_frame["edge"])
    nodes = list(nodes_frame["node"])
    edges_tubing = list(tubing_frame["edge"])
    nodes_tubing = list(tubing_nodes_frame)

    edgs = all([edge in edges for edge in edges_tubing])
    nods = all([node in nodes for node in nodes_tubing])

    if (edgs and nods) and edgs and nods:
        return edgs and nods, edgs, nods
    else:
        new_nodes = tubing_nodes_frame[[node not in nodes for node in nodes_tubing]]
        new_edges = tubing_edges_frame[[edge not in edges for edge in edges_tubing]]
        return edgs and nods, new_edges, new_nodes

def appendEdge(edgelst:list, edge_name:str, edgeNodes:pd.DataFrame, edgeProps:pd.DataFrame, reverse=False):
    ''' This function adds an edge to a list of edges. The edge is defined according to the format required by the graph. Data is taken from pandas dataframes containing nodes and
    properties of the edges. If the option reverse is set to true, then the edge is considered to be undirected and the reverse edge is also added to the list. This enable passage
    of the path in both directions in a directed graph. '''
    edgelst.append((edgeNodes.loc[edgeNodes["edge"] == edge_name, "start"].values[0], edgeNodes.loc[edgeNodes["edge"] == edge_name, "end"].values[0],
            {"name": edge_name, "designation": tuple((edgeNodes.loc[edgeNodes["edge"] == edge_name, "start"].values[0], edgeNodes.loc[edgeNodes["edge"] == edge_name, "end"].values[0])),
            "ends": edgeProps.loc[edgeProps["edge"] == edge_name, "ends"].values[0], "length": float(edgeProps.loc[edgeProps["edge"] == edge_name, "length"].values[0]), 
            "diameter": float(edgeProps.loc[edgeProps["edge"] == edge_name, "diameter"].values[0]), "dead_volume": float(edgeProps.loc[edgeProps["edge"] == edge_name, "dead_volume"].values[0]),
            "status": edgeProps.loc[edgeProps["edge"] == edge_name, "status"].values[0]}))
    if reverse == True:
        edgelst.append((edgeNodes.loc[edgeNodes["edge"] == edge_name, "end"].values[0], edgeNodes.loc[edgeNodes["edge"] == edge_name, "start"].values[0],
            {"name": edge_name, "designation": tuple((edgeNodes.loc[edgeNodes["edge"] == edge_name, "end"].values[0], edgeNodes.loc[edgeNodes["edge"] == edge_name, "start"].values[0])),
            "ends": edgeProps.loc[edgeProps["edge"] == edge_name, "ends"].values[0], "length": float(edgeProps.loc[edgeProps["edge"] == edge_name, "length"].values[0]),
            "diameter": float(edgeProps.loc[edgeProps["edge"] == edge_name, "diameter"].values[0]), "dead_volume": float(edgeProps.loc[edgeProps["edge"] == edge_name, "dead_volume"].values[0]),
            "status": edgeProps.loc[edgeProps["edge"] == edge_name, "status"].values[0]}))

# TODO: also check and load positions
def drawGraph(graph:nx.DiGraph, positions:dict, wlabels:bool=True):
    ''' This function draws and shows a graph. '''
    # ## Check types
    # # check positions and wlabels
    # if (not type(positions)==dict) or (not type(wlabels) == bool):
    #     print("positions:", type(positions), "wlabels:", type(wlabels))
    #     raise ValueError
    # check graph
    graph = getGraph(graph)
    nx.draw(graph, pos=positions, with_labels=wlabels)
    plt.show()

def getValveFromName(node_name:str, valvePositionDict=conf["CetoniDeviceDriver"]["valvePositionDict"]):
    ''' This function takes a name of a node (as string) as an input and returns the valve it belongs to. If the node does not belong to a valve. None is returned. '''
    ## Check types
    # check node_name
    if (not type(node_name)==str):
        raise ValueError
    # check valvePositionDict
    valvePositionDict = getValvePositionDict(valvePositionDict)
    # Get the valve from the node name
    valve = node_name[0:2]
    if valve in valvePositionDict.keys():
        # If valve corresponds to a valve, return it
        return valve
    else:
        # If the node does not belong to a valve, return NaN
        return np.NaN

def getEdgedictFromNodelist(nodelist:list, graph=conf["CetoniDeviceDriver"]["setup"]):
    ''' This function generates a dictionary of edges from a list of nodes. It takes a list of nodes as an input and returns a dictionary of edges with the name of the edge as
    a key. '''
    ## Chec input types
    # check nodelist
    if (not type(nodelist)==list):
        raise ValueError
    # check graph
    graph = getGraph(graph)

    edgesDict = {}
    for nd in nodelist:
        if (nodelist.index(nd)+1) < (len(nodelist)):
            edgesDict[graph[nd][nodelist[nodelist.index(nd)+1]]["name"]] = graph[nd][nodelist[nodelist.index(nd)+1]]    # https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.get_edge_data.html
    return edgesDict

def generateGraph(show:bool=True, save:bool=True, path_nodes:str=conf["graph"]["pathNodes"], path_edges:str=conf["graph"]["pathEdges"], path_tubing:str=conf["graph"]["pathTubing"], save_path:str=conf["graph"]["savePath"]):
    ''' This function generates a graph including the corresponding node positions and it can save both to the save_path according to the setting of the save parameter. '''
    ## Check input types
    # check show, save, path_nodes, path_edges, path_tubing and save_path
    if (not type(show)==bool) or (not type(save)==bool) or (not type(path_nodes)==str) or (not type(path_edges)==str) or (not type(path_tubing)==str) or (not type(save_path)==str):
        raise ValueError

    # Load the information regarding the nodes from nodes.csv to nodes_info.
    nodes_info = pd.read_csv(path_nodes, sep=";")
    # Load the information regarding the edges from edges.csv to nodes_info.
    edges_info = pd.read_csv(path_edges, sep=";")
    # Load the current configuration file for the tubing tubing.csv.
    tubing_config = pd.read_csv(path_tubing, sep=";")

    # Group information regarding nodes.
    nodes = []
    positions = {}
    # Go through all nodes in nodes.csv and add them and their position to a dictionary in order to add them to the graph lateron.
    for node in nodes_info["node"]:
        nodes.append((node, {"name": node,"position": eval(nodes_info.loc[nodes_info["node"] == node, "position_node"].values[0])})) # https://www.geeksforgeeks.org/python-convert-string-to-tuple/; conversion of str to tuple by using eval
        positions[node] = eval(nodes_info.loc[nodes_info["node"] == node, "position_node"].values[0])
    # Group information regarding edges.
    edges = []
    # Go through all the fixed edges in edges.csv and the edges contained in tubing.csv in order to generate the required dictionary containing the edges and their properties.
    for edge in edges_info.loc[edges_info["flexibility"] == "fixed", "edge"]:
        appendEdge(edges, edge, edges_info, edges_info, reverse=(edges_info.loc[edges_info["edge"] == edge, "restriction"].values[0] == "undirected"))
    for edge in tubing_config["edge"]:
        appendEdge(edges, edge, tubing_config, edges_info, reverse=(edges_info.loc[edges_info["edge"] == edge, "restriction"].values[0] == "undirected"))

    # Generate a graph named graph based on the data contained in tubing_info.
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    if show==True:
        drawGraph(graph, positions, wlabels=True)

    # If the parameter is set accordingly, save the graph and the positions to a pickle file. Else return the graph.
    if save==True:
        saveToFile(savePath=save_path, data=str(nx.to_dict_of_dicts(graph)))
        saveToFile(savePath=f"{str(save_path[0:-4])}_positions.txt", data=str(positions))
        return graph
    elif save==False:
        return graph

def getTotalQuantity(nodelist:list, quantity:str):   # Corresponds to networkx.path_weight.
    ''' This function calculates a total quantity (e.g. dead volume) for a list of nodes. It takes a list of nodes as an input,
    determines the respective dictionary of edges and returns the dead volume as a float. '''
    ## Check input types
    # check nodelist and quantity
    if (not type(nodelist)==list) or (not type(quantity)==str):
        raise ValueError

    edgedict = getEdgedictFromNodelist(nodelist=nodelist)
    quantityTotal = 0.0
    for edg in edgedict.keys():
        quantityTotal += edgedict[edg][quantity]
    return quantityTotal

def getValveSettings(nodelist:list, valvePositionDict:Union[str,dict]=conf["CetoniDeviceDriver"]["valvePositionDict"]):
    ''' Based on a list of nodes describing a path in the graph and a dict of valve positions, this function returns the required settings of the valves needed to realise
    this path, in case there are valves included in the path. Otherwise, an empty dict will be returned. The output is of type dict. '''
    ## Check input types
    # check nodelist
    if (not type(nodelist)==list):
        raise ValueError
    # check valvePositionDict
    valvePositionDict = getValvePositionDict(valvePositionDict)

    valveSettings = {}
    # Go through all nodes in the nodelist
    for node in nodelist:
        # split the node at the '.' to separate the valve designation from the position
        valve_pos = node.split('.')
        # if the list after the split has two elements,
        if len(valve_pos) == 2:
            # the valve is the first element
            valve = valve_pos[0]
            # the position is the second element
            pos = valve_pos[1]
            # if the valve is in the keys of the valvePositionDict, (this excludes nodes, which are not valves)
            if valve in valvePositionDict.keys():
                # if the valve is already included in the valve settings and the position is not 0
                if (valve in valveSettings.keys()) and (pos != "0"):
                    # the valve is passed a second time, which leads to an invalid path -> message
                    print("This path is not valid, because it passes the same valve multiple times.")
                # if the position is non-zero,
                elif pos != "0":
                    # add the position to the valve settings for the respective valve
                    valveSettings[valve] = valvePositionDict[valve][node]
                # if the position is zero, but not for a rotary valve,
                elif ('V' not in valve) and (pos == '0'):
                    # add the position to the valve settings for the respective valve
                    valveSettings[valve] = valvePositionDict[valve][node]
                # if the valve is a rotary valve and the position is zero, skip it
                elif ('V' in valve) and (pos == "0"):
                    pass
        # if the length of valve_pos is not two, skip this node, because it is not a valve with a position
        else:
            pass
    # return the valve settings
    return valveSettings

def pathIsValid(path:list, valvePositionDict:Union[str,dict]=conf["CetoniDeviceDriver"]["valvePositionDict"]):
    ''' This function checks a given path regarding its validity. If the path does not pass more than two nodes belonging to the same valve, it is considered being valid. '''
    ## Check input types
    # check path
    if (not type(path)==list):
        raise ValueError
    # check valvePositionDict
    valvePositionDict = getValvePositionDict(valvePositionDict)
    
    # Get the valves from the node names and save them in a list.
    valveList_orig = [getValveFromName(node, valvePositionDict) for node in path]
    # Transfer list to pandas dataframe.
    valveList = pd.DataFrame(valveList_orig)
    # Remove NaN values from the dataframe. These values originate from nodes that do not belong to a valve.
    valveList = valveList.dropna()
    # Get number of occurences of each valve in valveList
    occurance = valveList.value_counts()    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html
    if any([occ > 2 for occ in occurance]):
        # If any valve occures more than two times, the path is invalid.
        return False
    else:
        # Else it is valid.
        return True

def getSystemStatus(path:list=[], full:bool=True, graph:Union[str,nx.DiGraph]=conf["CetoniDeviceDriver"]["setup"]):
    ''' This function returns the status of all edges in the system. The output is a dict, which tells, if a certain edge is empty or filled with some liquid. If full is True, the status of all
    edges is returned, otherwise only the status of the edges in the requested path are returned. '''
    ## Check input types
    # check path and full
    if (not type(path)==list) or (not type(full)==bool):
        raise ValueError
    # check graph
    graph = getGraph(graph)
    
    # If the status is requested for the full system
    if full:
        # The status corresponds to the status for each edge
        status = nx.get_edge_attributes(graph, "status")    # https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.get_edge_attributes.html#networkx.classes.function.get_edge_attributes
    # If the status is only requested for a certain path
    else:
        # Initialize the status
        status = {}
        # Get the status of the full system
        statFull = nx.get_edge_attributes(graph, "status")
        # Get the edges involved in the relevant path
        edges = getEdgedictFromNodelist(nodelist=path, graph=graph)
        for edge in edges:
            # Change the status for each edge in the path
            status[edges[edge]["designation"]] = statFull[edges[edge]["designation"]]
    return status

def updateSystemStatus(path:list, graph:Union[str,nx.DiGraph]=conf["CetoniDeviceDriver"]["setup"]):
    ''' This function updates the status of edges in a path. It takes a path (list) as an input. The resulting status can be requested using the getSystemStatus function. '''
    ## Check input types
    # check path
    if (not type(path)==list):
        raise ValueError
    # check graph
    graph = getGraph(graph)
    
    # Get the edges of the relevant path
    edges = getEdgedictFromNodelist(nodelist=path, graph=graph)
    # Go through all the edges in the graph
    for edge in edges.keys():
        # Assign the origin of the path as the new status for each edge
        graph.edges[edges[edge]["designation"]]["status"] = path[0]
        try:
            # Try to update the status for the edge in the opposite direction in order to keep the status matching for the same edge
            graph[edges[edge]["designation"][1]][edges[edge]["designation"][0]]["status"] = path[0]
        except KeyError:
            # If there is no edge in the opposite direction, continue
            pass

def findPumps(pumps:dict, **conditions:str):
    ''' This function searches for a pump according to criteria given as arguments.
    The conditions must be of the format: key=column label in the dataframe, value contains the condition using the variable name "target".
    Secondary filtering requirements can be given in a key "secondary" in the conditions, which contains a dict. They keys of this dict
    must match the column names in the dataframe and the values must be functions like np.min or np.max. '''
    ## Check input types
    # check pumps
    if (not type(pumps)==list):
        raise ValueError
    
    # TODO: Test this function!!!
    # Gather the current information on all the pumps and their syringes
    pump_candidates = pd.DataFrame(columns=["pumpName", "pump", "maximumVolume", "minimumVolume", "status"])
    for pum in list(pumps.keys()):
        pcand = pd.DataFrame(data=np.array([pumps[pum].name, pumps[pum], pumps[pum].get_volume_max(), pumps[pum].syringe.minimum_volume_mL, pumps[pum].status], dtype=object)).transpose()
        pcand.columns = ["pumpName", "pump", "maximumVolume", "minimumVolume", "status"]
        pump_candidates = pd.concat([pump_candidates, pcand], axis=0, ignore_index=True)
    print(pump_candidates)
    # Initialize the found pumps as all candidates
    foundPumps = pump_candidates.copy()
    # Go through all the conditions keys
    for key in conditions.keys():
        if key != "secondary":
            # Define the target column, which is supposed to fulfill the respective condition. The label of the target column corresponds to the respective key of the condition
            target = foundPumps[key]
            # Filter foundPumps according to the condition at key. The evaluation uses the target definition from above
            foundPumps = foundPumps.loc[eval(conditions[key])]
    # If there are secondary conditions given (must be a dict type), meaning if there is a key named "secondary" in conditions
    if "secondary" in conditions.keys():
        # Go through all the keys in the secondary conditions
        for secKey in conditions["secondary"].keys():
            # Filter according to the secondary conditions
            foundPumps = foundPumps.loc[foundPumps[secKey]==conditions["secondary"][secKey](foundPumps[secKey])]
    # If there are no results remaining in foundPumps, print a message
    if len(foundPumps)==0:
        print("No pump fulfills the requirements.")
        # TODO: Raise an error here.
        return None
    # Reset the index of the resulting filtered dataframe
    foundPumps = foundPumps.reset_index()
    # Get the pumps column of the filtered dataframe and choose the element at index 0
    foundPumps = foundPumps.get("pump").array
    # Bring foundPumps into dict format for output
    output = {}
    for p in foundPumps:
        output[p.name] = p
    # Return the dictionary of the found pumps
    return output

def getOpenEnds(setup:Union[str,nx.DiGraph]=conf["CetoniDeviceDriver"]["setup"]):
    ''' This function finds the open ends in a graph. An open end is characterized by only one edge being attached to it. Since the graph is directed, but allows for
    bidirectional connections, some edges are added twice to cover both directions. Hence, an open End hat two edges with the same label. The function returns a list
    of the nodes, which are open ends. '''
    # ensure that setup is a graph
    setup = getGraph(setup)
    # initialise the list to collect the open edges
    openEnds = []
    ## Find all nodes with degree 2
    # get all the degrees for all notdes in the graph
    degrees = pd.DataFrame(setup.degree, columns=['nodes', 'degree'])   # https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.degree.html
    # nodes with degree zero do not have a connection to the graph and are therefore not reachable
    degreesNonZero = degrees.loc[degrees['degree'] != 0]
    # the open ends will have a degree of max. 2
    degrees2 = degreesNonZero.loc[degreesNonZero['degree'] <= 2]
    degrees2NoValves = degrees2.loc[['V' not in node for node in degrees2['nodes']]]
    ''' TODO: exclude open ends directly at valves. E.g. V1.6'''
    # for each of the nodes with a non-zero degree of less or equal 2
    for n in degrees2NoValves['nodes']:
        # get the outgoing edges
        outedges = list(setup.out_edges(n)) # https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.out_edges.html#networkx.DiGraph.out_edges
        # get the incoming edges
        inedges = list(setup.in_edges(n))   # https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.in_edges.html#networkx.DiGraph.in_edges
        # invert the inedges so they would represent the outedges, if the node is an open end
        invInedges = [(ie[1], ie[0]) for ie in inedges]
        # accept the node as an open end, if its outedges and inverse inedges are identical or one of them is empty
        if (outedges == invInedges) or (outedges == []) or (inedges == []):
            openEnds.append(n)
    return openEnds



    # TODO: Implement function to automatically find a practical way to realize an experiment. (Pump substance X from A to B via C.) This will require the following subfunctions:
    #       - Find the path with the least dead volume from A to B via C and D, where the sequence of C and D may matter or not.
    #       - Select a pump between different steps according to its status and the dead volume in the path from the relevant position to the pump
    #       - Insert nodes ( e.g. a pump) into a path.
    # TODO: Based on the functions mentioned above, implement an improved cleaning routine.

    # TODO: Get pumping steps automatically. No step by step instruction. Only from ... to ... this mixing ratio, this config. -> Do it.
