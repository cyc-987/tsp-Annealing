import numpy as np
import math

class tspProblem():
    def __init__(self, filepath):
        self.__checkTSPformat(filepath)
        self.__getMetaData(filepath)
        self.__convertToDistanceMatrix()
    
    #private funcs
    def __checkTSPformat(self, filepath):
        assert (filepath[-4:] == ".tsp")
    
    def __getMetaData(self, filepath):
        '''
        获取总节点数和坐标矩阵
        '''
        tsp = open(filepath, mode='r')
        #get numberof nodes
        line = tsp.readline()
        while(line[:9] != 'DIMENSION'): 
            line = tsp.readline()
        sp = line.split()
        nodes = [node for node in sp if node.isdigit()]
        numOfNodes = int(nodes[0])
        
        #get cordinate data
        while(line != 'NODE_COORD_SECTION\n'):
            line = tsp.readline()
        cordinates = np.zeros((numOfNodes, 2))
        for i in range(0, numOfNodes):
            line = tsp.readline()
            single = np.fromstring(line, dtype=float, sep=' ')
            cordinates[i,:] = single[1:3]
        
        #end
        tsp.close()
        self.numOfNodes = numOfNodes
        self.cordinates = cordinates
    
    def __convertToDistanceMatrix(self):
        '''
        计算距离矩阵
        '''
        # print(self.numOfNodes)
        # print(self.cordinates)
        distanceMatrix = np.zeros((self.numOfNodes, self.numOfNodes))
        for i in range(0, self.numOfNodes):
            for j in range(i, self.numOfNodes):
                distanceMatrix[i,j] = self.__distance(i,j)
                distanceMatrix[j,i] = distanceMatrix[i,j]
        
        #end
        self.distMatrix = distanceMatrix
    
    def __distance(self, i, j):
        dx = self.cordinates[i, 0] - self.cordinates[j, 0]
        dy = self.cordinates[i, 1] - self.cordinates[j, 1]
        return math.sqrt(dx**2 + dy**2)