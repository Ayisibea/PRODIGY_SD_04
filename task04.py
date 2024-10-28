import PySimpleGUI as sg

# Backtracking function to solve the Sudoku puzzle
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True  # Puzzle solved
    
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Reset if it doesn't lead to a solution

    return False

# Check if the number can be placed in the grid
def is_valid(board, num, row, col):
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

# Find an empty cell (denoted by 0)
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # Return row, col of empty cell
    return None

# Function to update the board from the GUI input
def update_board(values):
    board = []
    for row in range(9):
        board.append([int(values[f'{row}-{col}']) if values[f'{row}-{col}'] != '' else 0 for col in range(9)])
    return board

# Function to display the solved puzzle
def display_solved_board(window, board):
    for row in range(9):
        for col in range(9):
            window[f'{row}-{col}'].update(board[row][col])

# Define PySimpleGUI layout for Sudoku grid
def sudoku_layout():
    layout = []
    for row in range(9):
        row_layout = []
        for col in range(9):
            row_layout.append(sg.Input(size=(2, 1), key=f'{row}-{col}', justification='center'))
        layout.append(row_layout)
    layout.append([sg.Button('Solve'), sg.Button('Exit')])
    return layout

# Main function to run the Sudoku solver GUI
def main():
    # Create the window layout
    layout = sudoku_layout()
    window = sg.Window('Sudoku Solver', layout)
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == 'Solve':
            # Get the board from the inputs
            board = update_board(values)
            # Solve the Sudoku puzzle
            if solve_sudoku(board):
                # Update the GUI with the solved puzzle
                display_solved_board(window, board)
            else:
                sg.popup('No solution exists!')

    window.close()

if __name__ == '__main__':
    main()
