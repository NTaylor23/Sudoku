import numpy as np

class Solver:
    def __init__(self, board: np.array) -> None:
        self.board = board

    def start(self):
        self.solve(self.board)
        return self.board
        
    def solve(self, board):
        find = self.find_empty(board)
        
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve(board):
                    return True

                board[row][col] = 0

        return False
    
    def valid(self, board, num, pos):
        # Row
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Column
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Square
        square_x = pos[1] // 3
        square_y = pos[0] // 3

        for i in range(square_y * 3, square_y * 3 + 3):
            for j in range(square_x * 3, square_x * 3 + 3):
                if board[i][j] == num and (i,j) != pos:
                    return False

        return True
    
    def print_board(self, board):
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in range(len(board[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(board[i][j])
                else:
                    print(str(board[i][j]) + " ", end="")
                    
    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)  # row, col

        return None