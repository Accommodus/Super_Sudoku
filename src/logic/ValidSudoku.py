import math


def is_valid_sudoku(board):
    """
    Checks if an array is a valid sudoku solution

    Returns: Boolean
    """

    def is_valid_group(group):
        numbers = [num for num in group if num != 0]
        return len(numbers) == len(set(numbers))

    def is_valid_box(board, box_row, box_col, box_length):
        numbers = []
        for row in range(box_row, box_row + box_length):
            for col in range(box_col, box_col + box_length):
                num = board[row][col]
                if num != 0:
                    numbers.append(num)
        return is_valid_group(numbers)

    size = len(board)
    box_length = int(math.sqrt(size))

    # Check for 0s
    if 0 in board: return False

    # Check each row
    for row in board:
        if not is_valid_group(row):
            return False

    # Check each column
    for col in range(size):
        if not is_valid_group([board[row][col] for row in range(size)]):
            return False

    # Check each box
    for box_row in range(0, size, box_length):
        for box_col in range(0, size, box_length):
            if not is_valid_box(board, box_row, box_col, box_length):
                return False

    return True