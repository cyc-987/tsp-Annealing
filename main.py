import utils
import sa

problem = utils.tspProblem("./qa194.tsp")
# print(problem.distMatrix)
saProcess = sa.simulatedAnnealing(problem)
saProcess.initialSolution()
print(saProcess.solution)
print('total distance: ', saProcess.distance)

saProcess.run_listVersion()