import matplotlib.pyplot as plt
import numpy as np
import utils
import sa

class visualization():
    '''
    用于路径可视化
    '''
    def __init__(self, tsp: utils.tspProblem): # 此处的类型是tspProblem里的坐标
        self.fig, self.ax = plt.subplots()
        self.cordinates = tsp.cordinates
        self.scale = tsp.numOfNodes
        
        #draw
        self.drawPoints()
        self.show()
    
    def drawPoints(self):
        self.ax.scatter(self.cordinates[:,0], self.cordinates[:,1])
    
    def drawLines_listVersion(self, sa: sa.simulatedAnnealing):
        '''
        给一个解画线
        '''
        solution = sa.solution
        color = 'b'
        for i in range(0,self.scale):
            if i != self.scale-1:
                self.ax.plot([self.cordinates[solution[i],0], self.cordinates[solution[i+1], 0]], 
                             [self.cordinates[solution[i],1], self.cordinates[solution[i+1], 1]],
                             c=color)
            else:
                self.ax.plot([self.cordinates[solution[i],0], self.cordinates[solution[0], 0]], 
                             [self.cordinates[solution[i],1], self.cordinates[solution[0], 1]],
                             c=color) 
            plt.draw()
            plt.pause(0.1)
        plt.ioff()
        plt.show()
    
    def show(self):
        plt.ion()