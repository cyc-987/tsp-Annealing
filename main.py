import utils
import sa

problem = utils.tspProblem("./qa194.tsp")
# print(problem.distMatrix)
saProcess = sa.simulatedAnnealing(problem)
saProcess.initialSolution()
print('initial distance: ', saProcess.distance)

saProcess.run_listVersion()
print(saProcess.distance)