

#n queens
from chessboard import ChessBoardState

class NQueensAgent:
  def __init__(self):
    self.boardStates = []
    b = ChessBoardState(8)
    # b.displayBoard()
    self.boardStates.append(b)

    self.runAgent()

  def runAgent(self):s
    # self.boardStates[-1]
    while self.boardStates[-1].evaluateBoardState() > 0:
      #write some code to do a couple things 
      #-find the queens worth moving 

      #call the qList function on the current boardState [-1] and print the result 
      self.boardStates[-1].displayBoard()
      print(self.boardStates[-1].Qlist())
      
      break


      #-generate all the possible moves from the queens worth moving, and then find the new boardstate with the lowest amount of conflicts, append that boardstate to boardStates
      
agent = NQueensAgent()

agent.runAgent()
    