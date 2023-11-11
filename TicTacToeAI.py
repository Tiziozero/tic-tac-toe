import logic
#u suck dick bozo
def miniMax(board, depth, p1) :  
    score = logic.check_win(board, None)
    if score[0] == 2:
        return 1
    elif score[0] == 1:
        return -1
    Found = False
    for r in range(3) : 
        for c in range(3) : 
            if (board[r][c] == 0) :
                Found = True
    if not Found:
        return 0
    if p1:      
        best = -float("inf") 
        for r in range(3):          
            for c in range(3): 
                if (board[r][c]== 0): 
                    board[r][c] = 2  
                    best = max(best, miniMax(board, depth + 1, not p1)) 
                    board[r][c] = 0
        return best 
    else : 
        best = float("inf") 
        for r in range(3):          
            for c in range(3): 
                if (board[r][c] == 0):   
                    board[r][c] = 1
                    best = min(best, miniMax(board, depth + 1, not p1))
                    board[r][c] = 0
        return best

def AI(board) :  
    bestVal = -float("inf") 
    bestMove = ("banana", "1234")  
  
    for r in range(3):      
        for c in range(3): 
            if (board[r][c] == 0):   
                board[r][c] = 2 
                moveVal = miniMax(board, 0, False)  
                board[r][c] = 0 
                if (moveVal > bestVal):                 
                    bestMove = (r, c) 
                    bestVal = moveVal 
    board[bestMove[0]][bestMove[1]] = 2
    return board