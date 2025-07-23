class Grid:
    def __init__(self, width, height, default_value=None):
        """
        Initializes a new Grid object.

        Args:
            width (int): The number of columns in the grid.
            height (int): The number of rows in the grid.
            default_value: The default value to fill the grid with.
        """
        if not isinstance(width, int) or width <= 0:
            raise ValueError("Width must be a positive integer.")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Height must be a positive integer.")

        self.width = width
        self.height = height
        # Initialize the grid as a 2D list
        self._grid = [[default_value for _ in range(width)] for _ in range(height)]

    def get(self, x, y):
        """
        Returns the value at the specified coordinates (x, y).

        Args:
            x (int): The column index.
            y (int): The row index.

        Returns:
            The value at (x, y).
        Raises:
            IndexError: If x or y are out of bounds.
        """
        if not self._is_in_bounds(x, y):
            raise IndexError(f"Coordinates ({x}, {y}) are out of bounds.")
        return self._grid[y][x]

    def set(self, x, y, value):
        """
        Sets the value at the specified coordinates (x, y).

        Args:
            x (int): The column index.
            y (int): The row index.
            value: The value to set.
        Raises:
            IndexError: If x or y are out of bounds.
        """
        if not self._is_in_bounds(x, y):
            raise IndexError(f"Coordinates ({x}, {y}) are out of bounds.")
        self._grid[y][x] = value

    def _is_in_bounds(self, x, y):
        """
        Checks if the given coordinates are within the grid boundaries.

        Args:
            x (int): The column index.
            y (int): The row index.

        Returns:
            bool: True if in bounds, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def __str__(self):
        """
        Returns a string representation of the grid.
        """
        rows = []
        for row in self._grid:
            rows.append(" ".join(str(cell) for cell in row))
        return "\n".join(rows)

# Example Usage:
if __name__ == "__main__":
    my_grid = Grid(3, 3, default_value='.')
    print("Initial Grid:")
    print(my_grid)

    my_grid.set(0, 0, 'X')
    my_grid.set(1, 1, 'O')
    my_grid.set(2, 0, 'X')

    print("\nModified Grid:")
    print(my_grid)

    try:
        print(f"\nValue at (0,0): {my_grid.get(0, 0)}")
        my_grid.set(3, 0, 'Z') # This will raise an IndexError
    except IndexError as e:
        print(f"Error: {e}")