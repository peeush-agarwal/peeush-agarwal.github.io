# Intuition

To check if a Sudoku board is valid, we need to ensure that each digit appears only once in every row, column, and 3x3 sub-box. Using bitmasks allows us to efficiently track the presence of digits in each row, column, and box.

# Approach

- Use three arrays of bitmasks to track digits in rows, columns, and boxes.
- For each cell, if it contains a digit, check if the digit is already present in the corresponding row, column, or box using bitwise operations.
- If a duplicate is found, return `False`.
- Otherwise, set the corresponding bit in the row, column, and box bitmask.
- If no duplicates are found, return `True`.

# Complexity

- Time complexity:
$$O(1)$$ (since the board size is fixed at 9x9), but generally $$O(N^2)$$ for an NxN board.

- Space complexity:
$$O(1)$$ (only a few arrays of size 9 are used), but generally $$O(N)$$ for an NxN board.

# Code

```python
from typing import List

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        N = 9

        rows = [0] * N
        cols = [0] * N
        boxs = [0] * N

        for r in range(N):
            for c in range(N):
                if board[r][c] == ".":
                    continue

                pos = int(board[r][c]) - 1

                if rows[r] & (1 << pos):
                    return False
                rows[r] |= 1 << pos

                if cols[c] & (1 << pos):
                    return False
                cols[c] |= 1 << pos

                idx = (r // 3) * 3 + (c // 3)
                if boxs[idx] & (1 << pos):
                    return False
                boxs[idx] |= 1 << pos

        return True
```

[Back to Problem Statement](./index.md)
