# Intuition

To update the board for the Game of Life, we need to count live neighbors for each cell and apply the rules simultaneously. Using a copy of the board makes this straightforward, but it uses extra space.

# Approach

- Create a copy of the board to preserve the current state while updating cells.
- For each cell, count the number of live neighbors using the copy.
- Apply the four Game of Life rules to determine the next state for each cell.
- Update the original board in-place.

# Complexity

- Time complexity:
$$O(mn)$$, where $m$ and $n$ are the board dimensions (each cell and its neighbors are checked).

- Space complexity:
$$O(mn)$$, for the copy of the board.

# Code

```python
from typing import List

class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m = len(board)
        n = len(board[0])

        new_board = [[board[r][c] for c in range(n)] for r in range(m)]

        neighbors = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for row in range(m):
            for col in range(n):
                live_neighbors = 0
                for i, j in neighbors:
                    r = row + i
                    c = col + j

                    if (0 <= r < m) and (0 <= c < n) and (new_board[r][c] == 1):
                        live_neighbors += 1

                if (new_board[row][col] == 1) and (
                    live_neighbors < 2 or live_neighbors > 3
                ):
                    board[row][col] = 0

                if (new_board[row][col] == 0) and (live_neighbors == 3):
                    board[row][col] = 1
```

[Back to Problem Statement](./index.md)
