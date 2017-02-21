#!/usr/bin/env python

import collections

assignments = []

def cross(a, b):
    "Cross product of elements in a and elements in b."
    return [s+t for s in a for t in b]


# Global variables
ROWS = 'ABCDEFGHI'
COLS = '123456789'
BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI')
                              for cs in ('123','456','789')]
DIAGONALS = [[r+c for r, c in zip(ROWS, COLS)],
             [r+c for r, c in zip(ROWS[-1::-1], COLS)]]
UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAGONALS
UNITS = dict((s, [u for u in UNITLIST if s in u]) for s in BOXES)
PEERS = dict((s, set(sum(UNITS[s],[]))-set([s])) for s in BOXES)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in UNITLIST:
        twins = collections.defaultdict(list)
        for box in unit:
            value = values[box]
            if len(value) == 2:
                twins[value].append(box)
        twins = [(d, b) for d, b in twins.items() if len(b) == 2]
        if not twins:
            continue
        for digits, boxes in twins:
            for box in (set(unit) - set(boxes)):
                value = values[box].replace(digits[0], '').replace(digits[1], '')
                assign_value(values, box, value)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    return dict(zip(BOXES, (x if x != '.' else '123456789' for x in grid)))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(v) for v in values.values())
    line = '+'.join(['-'*(width*3)]*3)
    for r in ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers. Note this
    has the side effect of modifying the dictionary passed in.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, value in values.items():
        if len(value) == 1:
            for peer_box in PEERS[box]:
                peer_value = values[peer_box]
                if len(peer_value) > 1:
                    peer_value = peer_value.replace(value, '')
                    assign_value(values, peer_box, peer_value)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in UNITLIST:
        for digit in COLS:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def number_solved(values):
    """Compute the number of squares in the Sudoku puzzle that are solved."""
    return sum(1 for value in values.values() if len(value) == 1)


def contains_empty_square(values):
    """Checks that Sudoku puzzle does not contain squares without numbers."""
    for value in values.values():
        if not value:
            return True
    return False


def reduce_puzzle(values):
    """Iterate eliminate() and only_choice().

    If at some point, there is a box with no available values, return False. If
    the sudoku is solved, return the sudoku. If after an iteration of both
    functions, the sudoku remains the same, return the sudoku.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    num_solved_prev = number_solved(values)
    while True:
        eliminate(values)
        only_choice(values)
        naked_twins(values)
        num_solved_next = number_solved(values)
        if num_solved_prev == num_solved_next:
            break
        if contains_empty_square(values):
            return False
        num_solved_prev = num_solved_next
    return values


def search(values):
    """Using depth-first search and propagation, try all possible values."""
    if reduce_puzzle(values) is False:
        return False ## Failed earlier
    if all(len(value) == 1 for value in values.values()):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    _, box = min((len(v), b) for b, v in values.items() if len(v) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
