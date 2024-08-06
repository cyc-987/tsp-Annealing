import utils
import numpy as np
import random
import math

class simulatedAnnealing():
    def __init__(self, tspProblem: utils.tspProblem):
        # problem varibles
        self.tsp = tspProblem
        # solution varibles
        self.solution = np.zeros(self.tsp.numOfNodes, dtype=int) # store the solution
        self.distance = 0 # store the distance of the solution above
        self.selectMartix = selectMatrix(self) # use selectMatrix.matrix to get matrix itself
        # simulated Annealing parameters and varibles
        self.initialTemp = 10000
        self.currentTemp = self.initialTemp
        self.currentIteration = 0
        self.alpha = 0.997
        self.minTemp = 1e-12
        self.maxIteration = 1000000
        # other private varibles, used in the mid-calc parts
        self._recordTable = np.zeros((self.tsp.numOfNodes, 3),dtype=int)#selected,nodes,next
        random.seed()
    
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
        for i in range(1,self.tsp.numOfNodes):
            current = self.solution[i] = self._recordTable[current,2]
        self.calculateDistance_listVerion()
    
    def calculateDistance_listVerion(self):
        '''
        计算列表结果类型的距离
        '''
        dist = 0
        for i in range(0,self.tsp.numOfNodes):
            if i != self.tsp.numOfNodes-1:
                dist += self.tsp.distMatrix[self.solution[i],self.solution[i+1]]
            else:
                dist += self.tsp.distMatrix[self.solution[i],self.solution[0]]
        self.distance = dist
        
    
    def run_listVersion(self):
        '''
        主函数，使用列表跟踪解，随机反转更新邻域
        '''
        # initialization
        self.initialSolution()
        minDist = self.distance
        minSolution = self.solution
        oldDist = self.distance
        oldSolution = self.solution
        print('start sa')
        
        while(self.__checkEndCondition()):
            # generate next solution
            self.__nextSolution_listInverse()
            # calculate
            self.calculateDistance_listVerion()
            # check
            if self.distance < minDist: # better solution
                minDist = self.distance
                minSolution = self.solution
                print('accept_good')
            else: # accept at a percentage
                if self.__accept(self.distance - minDist): # accept
                    minDist = self.distance
                    minSolution = self.solution 
                    # print('accept_try')
                else: # retreat
                    self.distance = oldDist
                    self.solution = oldSolution
            # update
            oldDist = self.distance
            oldSolution = self.solution
            self.currentTemp *= self.alpha
            self.currentIteration += 1
            if self.currentIteration % 100 == 0: print(self.currentIteration)
            

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
    
    def __checkEndCondition(self):
        check = True
        if self.currentTemp < self.minTemp:
            check = False
        if self.currentIteration > self.maxIteration:
            check = False
        return check

    def __nextSolution_listInverse(self):
        i = random.randint(0, self.tsp.numOfNodes-2)
        j = random.randint(i+1, self.tsp.numOfNodes-1)
        self.solution[i:j] = list(reversed(self.solution[i:j]))
    
    def __accept(self, delta):
        rand = random.random()
        if rand < math.exp((-delta)/self.currentTemp):
            return True
        else: return False
    
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
    def convertSelectMatrixToSolution(self):
        '''
        与上面相反
        '''
        solution = np.zeros(self.scale, dtype=int)
        current = 0
        for i in range(1, self.scale):
            current = solution[i] = int([x for x in range(self.scale) if self.matrix[x,current] == 1][0])
        return solution
            