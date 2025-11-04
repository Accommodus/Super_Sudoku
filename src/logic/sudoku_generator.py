import random
import math


class SudokuGenerator:
    # Constructor
    def __init__(self, row_length, removed_cells):
        # Initialize a row_length x row_length board with zeros
        self.board = [[0] * row_length for _ in range(row_length)]
        self.removed_cells = removed_cells  # Number of cells to remove for puzzle
        self.row_length = row_length  # Size of the board
        self.box_length = int(math.sqrt(row_length))  # Size of boxes - sqrt of row_length

    # Return the current board state
    def get_board(self):
        return self.board

    # Check if a number can be placed in the given row
    def valid_in_row(self, row, num):
        return num not in self.board[row]

    # Check if a number can be placed in the given column
    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(self.row_length))

    # Check if a number can be placed in the 3x3 box
    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    # Check if placing num at (row, col) is valid
    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    # Fill a 3x3 box with numbers 1-9
    def fill_box(self, row, col):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums.pop()

    # Fill the diagonal 3x3 boxes to start puzzle generation
    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    # Remove a number of cells as specified by removed_cells
    def remove_cells(self):
        for _ in range(self.removed_cells):
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            # Ensure the cell isn't already empty before removing
            while self.board[row][col] == 0:
                row = random.randint(0, self.row_length - 1)
                col = random.randint(0, self.row_length - 1)
            self.board[row][col] = 0  # Set the cell's value to 0

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


# Print the board to the console
def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))