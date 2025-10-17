# Intuition

To rotate a matrix 90 degrees clockwise in-place, we can use two simple operations: transpose the matrix and then reflect each row horizontally.

# Approach

- First, transpose the matrix (swap rows and columns).
- Then, reflect each row horizontally (swap elements from left to right).
- Both operations are performed in-place, so no extra space is needed.

# Complexity

- Time complexity:
$$O(n^2)$$, where $n$ is the size of the matrix (each element is visited twice).

- Space complexity:
$$O(1)$$, since the rotation is done in-place.

# Code

```python
from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        def transpose():
            for i in range(n):
                for j in range(i):
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        def reflect():
            for i in range(n):
                for j in range(n // 2):
                    matrix[i][j], matrix[i][-j - 1] = matrix[i][-j - 1], matrix[i][j]

        n = len(matrix)
        transpose()
        reflect()
```

[Back to Problem Statement](./index.md)
