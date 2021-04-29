from queens import Queen
import random 
import copy as cp
import operator 

class ChessBoardState:
  def __init__(self,size):
    self.size = size

    self.board = []
    self.queens = []
    self.conflicts = []

    for i in range(size):
      row = []
      for j in range(size):
        row.append(".")
      self.board.append(row)

    #establish 1 queen per col in the board at a random row
    for i in range(size):
      queenRow = random.randint(0,size - 1)
      q = Queen(queenRow,i,i)
      self.queens.append(q)
      self.board[queenRow][i] = q
    
  def displayBoard(self):

    for i in range(len(self.board)):
      for j in range(len(self.board)):
        if(self.board[i][j] == "."):
          print(self.board[i][j],end = " ")
        else:
          print(self.board[i][j].id,end = " ")
      print("")

  #order: D
  def conflictIFS(self, Q1, Q2, index):
    if (self.conflicts[index][0].id == Q1.id and self.conflicts[index][1].id == Q2.id) or (self.conflicts[index][0].id == Q2.id and self.conflicts[index][1].id == Q1.id):
      return True

  #order: C
  def checkConflictExisting(self,q1,q2):
    for i in range(len(self.conflicts)):
      if self.conflictIFS(q1, q2, i):
        #print("already found")
        #print(self.conflicts[i][0].id,self.conflicts[i][1].id)
        return True
    return False

  #order: B
  def IFrow(self,i,j,queensTemp):
    if self.queens[i].row == queensTemp[j].row and not self.checkConflictExisting( self.queens[i], queensTemp[j])and not self.Hblock(self.queens[i], queensTemp[j]):
      return True
    return False 

  #order: B
  def IFcol(self,i,j,queensTemp):
    if self.queens[i].col == queensTemp[j].col and not self.checkConflictExisting( self.queens[i], queensTemp[j]) and not self.Vblock(self.queens[i], queensTemp[j]):
      return True
    return False 

  def IFdiagonal(self,i,j,queensTemp):
    #find the x and y components of the distance between self.queens[i] and queensTemp[j]
    if abs(self.queens[i].row - queensTemp[j].row) == abs(self.queens[i].col - queensTemp[j].col):
      if not self.checkConflictExisting(self.queens[i], queensTemp[j]) and not self.DiagonalBlock(self.queens[i], queensTemp[j]):
        return True
    return False
    

  #order: A
  def evaluateBoardState(self):
    for i in range(len(self.queens)): 
      queensTemp = cp.copy(self.queens)
      
      queensTemp.remove(self.queens[i])
      
      for j in range(len(queensTemp)):
        if self.IFrow(i,j,queensTemp):
          self.conflicts.append((self.queens[i],queensTemp[j]))
        if self.IFcol(i,j,queensTemp):
          self.conflicts.append((self.queens[i],queensTemp[j]))
        if self.IFdiagonal(i,j,queensTemp):
          self.conflicts.append((self.queens[i],queensTemp[j]))

    #print("conflicts : ",len(self.conflicts))

    #self.conflictDebug(self.conflicts)
    return (len(self.conflicts))

  def conflictDebug(self,conflicts):
    for i in range(len(conflicts)):
      print(str(conflicts[i][0].id) + " conflicts with " + str(conflicts[i][1].id))
   

  #blocking checks 
  def Hblock(self,q1,q2):
    qTemp = cp.copy(self.queens)
    qTemp.remove(q1)
    qTemp.remove(q2)
 
    for i in range(len(qTemp)):
      if qTemp[i].row == q2.row:
        #positive dist 
        if q1.col < q2.col:
          if qTemp[i].col > q1.col and qTemp[i].col < q2.col:
            return True
        else:
          if qTemp[i].col < q1.col and qTemp[i].col > q2.col:
            return True
    return False

  def Vblock(self,q1,q2):
    qTemp = cp.copy(self.queens)
    qTemp.remove(q1)
    qTemp.remove(q2)

    for i in range(len(qTemp)):
      if qTemp[i].col == q2.col:
        #positive dist 
        if q1.row < q2.row:
          if qTemp[i].row > q1.row and qTemp[i].row < q2.row:
            return True
        else:
          if qTemp[i].row < q1.row and qTemp[i].row > q2.row:
            return True
    return False

  def DiagonalBlock(self,q1,q2):
    qTemp = cp.copy(self.queens)
    qTemp.remove(q1)
    qTemp.remove(q2)


    xDist = q1.col - q2.col
    yDist = q1.row - q2.row

    # Left(top) to right(down) diagonal blockade
    #Q1 is 5, Q2 is 7, xDist is -2, yDist is -2

    if (xDist < 0) and (yDist < 0):
      for i in range(len(qTemp)):
        # qTemp[i] is 3, q2 is 7
        if ((qTemp[i].col - q2.col) < 0) and ((qTemp[i].row - q2.row) < 0):
          if ((qTemp[i].col - q2.col) < xDist) and ((qTemp[i].row - q2.row) < yDist):
            return True
    
    # right to left diagonal blockade
    #Q1 is 6, Q2 is 7, xDist is -1, yDist is 1
    if (xDist < 0) and (yDist > 0):
      for i in range(len(qTemp)):
        # qTemp[i] is 4, q2 is 7
        if ((qTemp[i].col - q2.col) < 0) and ((qTemp[i].row - q2.row) > 0):
          if ((qTemp[i].col - q2.col) < xDist) and ((qTemp[i].row - q2.row) < yDist):
            return True

    #Q1 is 3, Q2 is 5, xDist is -2, yDist is -4
    #xDist for 3 and 7 is -4, yDist for 3 and 7 is -4
    if (xDist < 0) and (yDist < 0):
      for i in range(len(qTemp)):
        # qTemp[i] is 4, q2 is 7
        if ((q1.col - qTemp[i].col) < 0) and ((q1.row - qTemp[i].row) < 0):
          if ((q1.col - qTemp[i].col) < xDist) and ((qTemp[i].row - q2.row) <= yDist):
            return True

    # Q1 is 5, Q2 is 3, xDist is 2, yDist is 2
    # xDist for 5 and 2 is 3, yDist for 5 and 2 is 3
    if (xDist > 0) and (yDist > 0):
      for i in range(len(qTemp)):
        # qTemp[i] is 4, q2 is 7
        if ((q1.col - qTemp[i].col) > 0) and ((q1.row - qTemp[i].row) > 0):
          if ((q1.col - qTemp[i].col) > xDist) and ((qTemp[i].row - q2.row) > yDist):
            return True
            
    return False

  #find and return the queen causing the most conflicts, if there are ties just return a random one 
  
  def Qlist(self):
    d = {}
    for i in range(len(self.conflicts)):
      if self.conflicts[i][0].id not in d:
        d[self.conflicts[i][0].id] = 1
      else:
        d[self.conflicts[i][0].id] += 1


      if self.conflicts[i][1].id not in d:
        d[self.conflicts[i][1].id] = 1
      else:
        d[self.conflicts[i][1].id] += 1
    
    #d now has a map of all the queens and the numbers of conflicts 
    #find the maximum value in a dictionary 
    return max(d.items(), key = operator.itemgetter(1))[0]

  
  #this function returns a new boardstate with a lower heuristic evaluation than the current boardstate, we need the id of the queen that we're going to move to generate the new boardstate 


  def generate_board_state(self, queen_id):
    #make a copy of self
    new_board_state = cp.copy(self)

    #write code for iterating over all the possible directions we could move the queen 
    
    #horizontal  
    #find the bounds of positions in the row we can access 
    currQueen = self.return_queen(queen_id)
    # Top left to bottom right is Left Bound
    # Bottom left to top right is Righ Bound
    Hbounds = (0,len(self.grid[currQueen.row]) - 1)
    Vbounds = (0,len(self.grid[currQueen.col]) - 1)
    Lbounds = (0,len(self.grid[currQueen.row]) - 1)
    Rbounds = (0,len(self.grid[currQueen.col]) - 1)

    #find if any other queens exist in the row with us, if they do exist then lower the bounds
    ql = cp.copy(self.queens)
    ql.remove(currQueen)
    
    for i in range(len(self.ql)):
          
      #horizontal bounds checker
      if ql[i].row == currQueen.row and (ql[i].col in range(Hbounds[0], Hbounds[1])):
        #if there is a queen in the same row, adjust the bounds to properly reflect the legal possible moves 
        if ql[i].col < currQueen.col:
          Hbounds[0] = q1[i].col + 1
        else:
          Hbounds[1] = ql[i].col - 1
      
      #vertical bounds checker
      if ql[i].col == currQueen.col and (ql[i].row in range(Vbounds[0], Vbounds[1])):
        if ql[i].row < currQueen.row:
          Vbounds[0] = q1[i].row + 1
        else:
          Vbounds[1] = q1[i].row - 1
      
      #diagonal bound checker
      if abs(currQueen.col - ql[i].col) == abs(currQueen.row - ql[i].row):
        if (currQueen.col < ql[i].col and currQueen.row > ql[i].row) or (currQueen.col > ql[i].col and currQueen.row < ql[i].row):
          if ql[i].row in range(Rbounds[0], Rbounds[1]):
            if ql[i].row > currQueen.row:
              Rbounds[1] = ql[i].row - 1
            else:
              Rbounds[0] = ql[i].row + 1
        else:
          if ql[i].row in range(Lbounds[0], Lbounds[1]):
            if ql[i].col < currQueen.col:
              Lbounds[0] = ql[i].col + 1
            else:
              Lbounds[1] = ql[i].col - 1

  #write a function that takes a queen id, and return the queen 
  def return_queen(self, queen_id):
    for i in range(len(self.queens)):
      if self.queens[i].id == queen_id:
        return self.queens[i]

  #write a function that takes a queen, and moves it to a new position
  def move_queen(self, queen, row, column):
    self.grid[queen.row][queen.col] = "."
    self.queen.row = row
    self.queen.col = column
    self.grid[queen.row][queen.column] = queen.id