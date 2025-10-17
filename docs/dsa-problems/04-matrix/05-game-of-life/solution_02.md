# Intuition

To update the board for the Game of Life in-place, we need to ensure all cells are updated simultaneously. We can use special markers to encode state transitions without using extra space.

# Approach

- For each cell, count live neighbors using `abs(board[r][c]) == 1` to handle intermediate states.
- Use `-1` to mark cells that change from live to dead, and `2` for cells that change from dead to live.
- After processing all cells, update the board: set cells to `1` if their value is positive, otherwise to `0`.

# Complexity

- Time complexity:
$$O(mn)$$, where $m$ and $n$ are the board dimensions (each cell and its neighbors are checked).

- Space complexity:
$$O(1)$$, since the update is done in-place.

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

        # Replace with -1 when changing from 1 -> 0
        # Replace with 2 when changing from 0 -> 1

        for row in range(m):
            for col in range(n):
                live_neighbors = 0
                for i, j in neighbors:
                    r = row + i
                    c = col + j

                    if (0 <= r < m) and (0 <= c < n) and (abs(board[r][c]) == 1):
                        live_neighbors += 1

                if (board[row][col] == 1) and (
                    live_neighbors < 2 or live_neighbors > 3
                ):
                    board[row][col] = -1

                if (board[row][col] == 0) and (live_neighbors == 3):
                    board[row][col] = 2

        for row in range(m):
            for col in range(n):
                board[row][col] = 1 if board[row][col] > 0 else 0
```

[Back to Problem Statement](./index.md)
