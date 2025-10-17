# Intuition

To traverse a matrix in spiral order, we can peel off the outer boundary layer by layer, moving inward after each full traversal of the current boundary.

# Approach

- Use four pointers to track the current boundaries: top (`rs`), bottom (`re`), left (`cs`), and right (`ce`).
- For each layer:
    - Traverse the top row from left to right.
    - Traverse the right column from top to bottom.
    - Traverse the bottom row from right to left (if not already traversed).
    - Traverse the left column from bottom to top (if not already traversed).
- After each layer, move the boundaries inward and repeat until all elements are visited.

# Complexity

- Time complexity:
$$O(m \times n)$$, where $m$ and $n$ are the matrix dimensions (each element is visited once).

- Space complexity:
$$O(1)$$ (excluding the output list).

# Code

```python
from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])
        res = []

        def boundary_items(rs, re, cs, ce):
            # First row
            res.extend([matrix[rs][c] for c in range(cs, ce + 1)])

            # Last col
            res.extend([matrix[r][ce] for r in range(rs + 1, re)])

            if rs != re:
                # Bottom row
                res.extend([matrix[re][c] for c in range(ce, cs - 1, -1)])

            if cs != ce:
                # First col
                res.extend([matrix[r][cs] for r in range(re - 1, rs, -1)])

        rs, re = 0, m - 1
        cs, ce = 0, n - 1

        while (rs <= re) and (cs <= ce):
            boundary_items(rs, re, cs, ce)

            rs += 1
            re -= 1
            cs += 1
            ce -= 1

        return res
```

[Back to Problem Statement](./index.md)
