# Rotate Image

## Problem Statement

Given an `n x n` 2D matrix representing an image, rotate the image by 90 degrees clockwise.

- The rotation must be performed **in-place**; modify the input matrix directly.
- **Do not** allocate another 2D matrix for the rotation.

### Example 1

![Matrix Rotation 1](./mat1.jpg)

**Input:**  
`matrix = [[1,2,3],[4,5,6],[7,8,9]]`

**Output:**  
`[[7,4,1],[8,5,2],[9,6,3]]`

### Example 2

![Matrix Rotation 2](./mat2.jpg)

**Input:**  
`matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]`

**Output:**  
`[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]`

### Constraints

- `n == matrix.length == matrix[i].length`
- `1 <= n <= 20`
- `-1000 <= matrix[i][j] <= 1000`

## Code Template

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach first transposes the matrix and then reverses each row to achieve the 90-degree clockwise rotation. The time complexity is O(n^2) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
