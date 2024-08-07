import matplotlib.pyplot as plt
import numpy as np

class visualization():
    '''
    用于路径可视化
    '''
    def __init__(self, tsp): # 此处的类型是tspProblem里的坐标
        self.fig, self.ax = plt.subplots()
        self.cordinates = tsp.cordinates
        self.scale = tsp.numOfNodes
        
        #draw
        self.__drawPoints()
        self.__show()
    
    # public funcs
    def update(self, sa, pauseTime):
        '''
        更新路径，原理是擦除并重绘
        '''
        self.__clear()
        self.__drawPoints()
        # self.__midUpdate(pauseTime)
        self.__setTitle(sa.currentIteration)
        self.__drawLines_listVersion(sa)
        self.__midUpdate(pauseTime)
    
    def end(self):
        '''
        停止更新路径
        '''
        self.__endUpdate()
        
    # private funcs
    def __drawPoints(self):
        self.ax.scatter(self.cordinates[:,0], self.cordinates[:,1])
    
    def __drawLines_listVersion(self, sa):
        '''
        给一个解画线
        '''
        solution = sa.solution
        color = 'c'
        for i in range(0,self.scale):
            if i != self.scale-1:
                self.ax.plot([self.cordinates[solution[i],0], self.cordinates[solution[i+1], 0]], 
                             [self.cordinates[solution[i],1], self.cordinates[solution[i+1], 1]],
                             c=color)
            else:
                self.ax.plot([self.cordinates[solution[i],0], self.cordinates[solution[0], 0]], 
                             [self.cordinates[solution[i],1], self.cordinates[solution[0], 1]],
                             c=color) 
    def __setTitle(self, it):
        self.ax.set_title(('Iteration:'+str(it)))
    
    def __midUpdate(self, pause):
        # plt.draw()
        plt.pause(pause)
    def __endUpdate(self):
        plt.ioff()
        plt.show()
    def __clear(self):
        self.ax.cla()
    
    def __show(self):
        plt.ion()