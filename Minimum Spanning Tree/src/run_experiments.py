#!/usr/bin/python
# CSE6140 HW2
# This is an example of how your experiments should look like.
# Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
from re import U
import time
import sys

#import required libraries
import networkx as nx
import heapq
from collections import deque

MST = nx.Graph() #global variable

class RunExperiments:
    def parse_edges(self, filename):
        # Write this function to parse edges from graph file to create your graph object
        file = open(filename, 'r')
        file.readline()
        #using multigraph due to multiple edges between a set of vertices
        multiG = nx.MultiGraph()
        line = file.readline()
        while line:
            ls = line.split(" ")
            multiG.add_edge(int(ls[0]), int(ls[1]), weight = int(ls[2]))
            line = file.readline()
        return multiG
        
    def computeMST(self, G):
        # Write this function to compute total weight of MST
        multiG = G.copy()
        G = nx.Graph()

        #converting a multigraph into a graph by picking the minimum weighted egde between vertices 
        for u in range(multiG.number_of_nodes()):
            for v in multiG[u]:
                min_edge_wt = float('inf')
                if(v > u):
                    for k in multiG[u][v]:
                        if multiG[u][v][k]['weight'] < min_edge_wt :
                            min_edge_wt = multiG[u][v][k]['weight']
                    G.add_edge(u, v, weight = min_edge_wt)
        
        #prim's algorithm for computing MST

        #Priority Queue starting from node 0 is our set of explored nodes S
        #Queue entries are (weight of node u from set S, u)
        Q = [(0, 0)]
        heapq.heapify(Q)
        pred = [None]*G.number_of_nodes() #maintaining predecessor of each node in S

        while Q: #while priority queue has nodes left in it
            wt_u, u = heapq.heappop(Q) #getting the element with the least weight from Q
            if(MST.has_node(u) == False): 
                if(u == 0): #to add the first node to MST
                    MST.add_node(u)
                else: #for all other nodes
                    MST.add_edge(u, pred[u], weight = wt_u)
                for nbr in G.neighbors(u): #all neighbours of u are weighed from S and added to queue
                    if nbr not in MST:
                        heapq.heappush(Q, (G[u][nbr]['weight'], nbr))
                        pred[nbr] = u 

        total_weight = MST.size(weight="weight")
        return int(total_weight)

    def recomputeMST(self, u, v, weight, G):
        # Write this function to recompute total weight of MST with the newly added edge

        #performing BFS to find path between u and v
        visited = set([u])
        pred = {}
        q = deque([u])
        while q:
            curr = q.popleft()
            for nxt in MST.neighbors(curr):
                if nxt not in visited:
                    visited.add(nxt) 
                    pred[nxt] = curr #keeping track of predecessors in the path 
                    if(nxt == v): break 
                    q.append(nxt) #keep exploring till we find v

        #loop over the path from v to u, setting v to its predecessor at every iteration, to find the heaviest edge in the path
        max_wt = 0 #weight of the heaviest edge
        max1, max2 = None, None #vertices of the heaviest edge
        vx = v #copy of v
        while vx!= u:
            new_wt = MST[vx][pred[vx]]['weight']
            if new_wt > max_wt:
                max_wt = new_wt
                max1, max2 = vx, pred[vx]
            vx = pred[vx]
        
        #replace with new edge if heaviest edge between u and v in current MST is heavier than new edge
        if max_wt > weight:
            MST.remove_edge(max1, max2)
            MST.add_edge(u, v, weight = weight)

        updated_weight = MST.size(weight='weight')
        return int(updated_weight)

    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        # Construct graph
        G = self.parse_edges(graph_file)

        start_MST = time.time()  # time in seconds
        # call MST function to return total weight of MST
        MSTweight = self.computeMST(G)
        total_time = (time.time() - start_MST) * \
            1000  # to convert to milliseconds
        # Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time) + '\n')

        changes_time = 0

        # Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = time.time()
                new_weight = self.recomputeMST(u, v, weight, G)
                # to convert to milliseconds
                total_recompute = (time.time() - start_recompute) * 1000

                # write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute) + '\n')

if __name__ == '__main__':
    # run the experiments
    runexp = RunExperiments()
    runexp.main()
