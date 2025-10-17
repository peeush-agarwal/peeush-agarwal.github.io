# Intuition

To set matrix zeroes in-place with constant space, we can use the first row and first column as markers to indicate which rows and columns should be zeroed. Special care is needed for the first row and column themselves.

# Approach

- Use the first row and first column to mark zeroes for other rows and columns.
- Use a separate flag to track if the first column should be zeroed.
- In the first pass, mark the first row/column if a zero is found.
- In the second pass, set cells to zero based on the markers.
- Finally, zero out the first row and/or column if needed.

# Complexity

- Time complexity:
$$O(mn)$$, where $m$ and $n$ are the matrix dimensions (each cell is visited twice).

- Space complexity:
$$O(1)$$, since the marking is done in-place.

# Code

```python
from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        is_col = False
        m = len(matrix)
        n = len(matrix[0])

        for i in range(m):
            if matrix[i][0] == 0:
                is_col = True

            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if not matrix[i][0] or not matrix[0][j]:
                    matrix[i][j] = 0

        if matrix[0][0] == 0:
            for j in range(n):
                matrix[0][j] = 0

        if is_col:
            for i in range(m):
                matrix[i][0] = 0
```

[Back to Problem Statement](./index.md)
