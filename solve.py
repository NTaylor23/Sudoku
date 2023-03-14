import numpy as np

class Solver:
    def __init__(self, board: np.array) -> None:
        self.board = board

    def start(self) -> any:
        """Verify that the board is valid, and then proceed to solve."""
        if self.verify_sudoku_board(self.board):
            self.solve(self.board)
            return self.board
        else:
            return None
    
    def contains_duplicate(self, row: list) -> bool:
        """ Check if the row contains a duplicate number, not including 0s."""
        row = list(row)
        for i in range(1, 10):
            if row.count(i) > 1:
                return False
        return True
    
    def verify_sudoku_board(self, board) -> bool:
        # Check rows
        for row in board:
            if not self.contains_duplicate(row):
                return False

        # Check columns
        for col in range(9):
            if not self.contains_duplicate([row[col] for row in board]):
                return False

        # Check squares
        for row in range(3):
            for col in range(3):
                square = [board[row*3 + i][col*3 + j] for i in range(3) for j in range(3)]
                if not self.contains_duplicate(square):
                    return False

        return True
        
        
    def solve(self, board) -> bool:
        """Recursively check each possible match and accumulate towards a solution."""
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
    
    def find_empty(self, board):
        """Find the next empty square."""
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)  # row, col

        return None