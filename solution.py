assignments = []

class Global:
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(Global.rows, Global.cols)

    row_units = [cross(r, Global.cols) for r in Global.rows]
    column_units = [cross(Global.rows, c) for c in Global.cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = Global.row_units + Global.column_units + Global.square_units
    units = dict((s, [u for u in Global.unitlist if s in u]) for s in Global.boxes)
    peers = dict((s, set(sum(Global.units[s],[]))-set([s])) for s in Global.boxes)


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

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(a, b):
    "Cross product of elements in a and elements in b."
    return [s+t for s in a for t in b]

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
    return dict(zip(Global.boxes, (x if x != '.' else '123456789' for x in grid)))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in Global.boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in Global.rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in Global.cols))
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
            for peer_box in Global.peers[box]:
                peer_value = values[peer_box].replace(value, '')
                assign_value(values, peer_box, peer_value)
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in Global.unitlist:
        boxes = [box for box in unit if len(values[box]) > 1]
        counter = collections.Counter()
        for box in boxes:
            counter.update(values[box])
        digit, count = counter.most_common()[-1]
        if count > 1:
            continue
        for box in boxes:
            if digit in values[box]:
                assign_value(values, box, digit)
                break
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
    while True:
        # Check how many boxes have a determined value
        num_solved = number_solved(values)

        # Use the Eliminate Strategy
        eliminate(values)

        # Use the Only Choice Strategy
        only_choice(values)

        # If no new values were added, stop the loop.
        if num_solved == number_solved(values):
            break

        # Sanity check, return False if there is a box with zero available values:
        if contains_empty_square(values):
            return False
    return values

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

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
