import numpy as np
from tabulate import tabulate

class Tableau:
    def __init__(self, zRow = None, zCol = None, A = None, typeSolve = 'primal', c = None, initBasis = None):
        self.zRow = zRow
        self.zCol = zCol
        self.A = A
        self.typeSolve = typeSolve
        self.n = len(zRow)
        self.m = len(zCol)
        self.inBasis = initBasis
        self.pivotCol = None
        self.pivotRow = None
        self.cost = c
        self.cc = 0
        self.calculateCost()



    def solve(self, printSteps = True, printFinal = True, step = 1):
        if step != 1:
            print()
        print(f'Step {step}:')
        self.printTableau()
        self.findPivot()
        if self.pivotCol == None:
            print('\nDone!')
            return
        factor = self.zRow[self.pivotCol]/self.A[self.pivotRow][self.pivotCol] * -1
        for i, val in enumerate(self.zRow):
            self.zRow[i] = val + factor*self.A[self.pivotRow][i]
        for i, row in enumerate(self.A):
            if i == self.pivotRow:
                continue
            factor = row[self.pivotCol] / self.A[self.pivotRow][self.pivotCol] * -1
            for j, val in enumerate(row):
                self.A[i][j] = val + factor*self.A[self.pivotRow][j]
            self.zCol[i] = self.zCol[i] + factor*self.zCol[self.pivotRow]
        factor = 1/self.A[self.pivotRow][self.pivotCol]
        for i, val in enumerate(self.A[self.pivotRow]):
            self.A[self.pivotRow][i] = val*factor
        self.zCol[self.pivotRow] = self.zCol[self.pivotRow]*factor
        self.inBasis[self.pivotRow] = self.pivotCol + 1
        self.calculateCost()
        step += 1
        self.solve(printSteps, printFinal, step)

    def calculateCost(self):
        self.cc = 0
        for i, b in enumerate(self.inBasis):
            self.cc += self.cost[b-1]*self.zCol[i]
        self.cc *= -1


    def findPivot(self):
        self.pivotCol = None
        for i, val in enumerate(zRow):
            if val < 0:
                self.pivotCol = i
                break
        if self.pivotCol == None:
            return
        smallestJ = None
        smallestRatio = None
        for j, row in enumerate(A):
            if row[self.pivotCol] <= 0:
                continue
            elif smallestJ == None or self.zCol[j]/row[self.pivotCol] < smallestRatio:
                smallestJ = j
                smallestRatio = self.zCol[self.pivotCol]/row[self.pivotCol]
        self.pivotRow = smallestJ

    def printTableau(self):
        arr = [['c'] + [self.cc] + zRow]
        for i, row in enumerate(A):
            r = [f'x{self.inBasis[i]}'] + [self.zCol[i]] + row
            arr += [r]
        header = ['', '']
        for i in range(self.n):
            header += [f'x{i + 1}']
        print(tabulate(arr, headers = header))

if __name__ == '__main__':
    zRow = [-10, -12, -12, 0, 0, 0]
    zCol = [20, 20, 20]
    A = [[1, 2, 2, 1, 0, 0],
          [2, 1, 2, 0, 1, 0],
          [2, 2, 1, 0, 0, 1]]
    c = [-10, -12, -12, 0, 0, 0]
    initBasis = [4, 5, 6]
    t = Tableau(zRow = zRow, zCol = zCol, A = A, c = c, initBasis = initBasis)
    t.solve()
