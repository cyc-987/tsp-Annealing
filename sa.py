import utils
import numpy as np

class simulatedAnnealing():
    def __init__(self, tspProblem: utils.tspProblem):
        # problem varibles
        self.tsp = tspProblem
        # solution varibles
        self.solution = np.zeros(self.tsp.numOfNodes, dtype=int) # store the solution
        self.distance = 0 # store the distance of the solution above
        self.selectMartix = selectMatrix(self) # use selectMatrix.matrix to get matrix itself
        # other private varibles, used in the mid-calc parts
        self._recordTable = np.zeros((self.tsp.numOfNodes, 3),dtype=int)#selected,nodes,next
    
    # public funcs
    def initialSolution(self):
        '''
        生成初始解，目前使用贪心算法
        '''
        #使用贪心算法，每次寻找最近的一个点
        current = 0
        self._recordTable[current,0] = 1
        for i in range(0,self.tsp.numOfNodes):
            if i != self.tsp.numOfNodes-1:
                self._recordTable[current,2] = self.__findNext_initial(current)
            else:
                self._recordTable[current,2] = 0
            current = int(self._recordTable[current,2])
            # print(current)
            self._recordTable[current,0] = 1
        
        #finals
        self.calculateResultandStore()
        self.selectMartix.convertSolutionToSelectMatrix(self.solution)
    
    def calculateResultandStore(self):
        '''
        计算总路径长度并且保存路径
        '''
        # make result
        current = 0
        dist = 0
        for i in range(1,self.tsp.numOfNodes):
            current = self.solution[i] = self._recordTable[current,2]
        # calculate distance
        for i in range(0,self.tsp.numOfNodes):
            if i != self.tsp.numOfNodes-1:
                dist += self.tsp.distMatrix[self.solution[i],self.solution[i+1]]
            else:
                dist += self.tsp.distMatrix[self.solution[i],self.solution[0]]
        self.distance = dist

    #private funcs
    def __findNext_initial(self, current):
        nodeIndex = 0
        minDistance = 10e8
        for i in range(0,self.tsp.numOfNodes):
            if current == i : continue
            elif self.tsp.distMatrix[current, i] < minDistance and self._recordTable[i, 0] == 0:
                nodeIndex = i
                minDistance = self.tsp.distMatrix[current, i]
        return int(nodeIndex)
    
class selectMatrix():
    '''
    选择矩阵类，用于构造、生成新解等
    '''
    def __init__(self, sa: simulatedAnnealing):
        self.sa = sa
        self.scale = sa.tsp.numOfNodes
        self.matrix = np.zeros((self.scale, self.scale), dtype=int)
    
    def convertSolutionToSelectMatrix(self, solution):
        '''
        转换初始解（数组）到选择矩阵（0-1形式）
        '''
        current = solution[0]
        for i in range(0, self.scale):
            if i != self.scale-1:
                self.matrix[solution[i+1],current] = 1
                current = solution[i+1]
            else:
                self.matrix[solution[0], current] = 1