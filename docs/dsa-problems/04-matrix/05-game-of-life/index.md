# Game of Life

## Problem Statement

Conway's Game of Life is a cellular automaton played on an m x n grid of cells, where each cell is either live (`1`) or dead (`0`). Each cell interacts with its eight neighbors (horizontal, vertical, and diagonal) according to these rules:

1. Any live cell with fewer than two live neighbors dies (under-population).
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies (over-population).
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).

All cells are updated simultaneously based on the current state.

**Task:**  
Given the current state of the board as a 2D array, update the board to its next state according to the rules above. You do not need to return anything; update the board in-place.

**Examples:**

Example 1:  
Input: `board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]`  
Output: `[[0,0,0],[1,0,1],[0,1,1],[0,1,0]]`

Example 2:  
Input: `board = [[1,1],[1,0]]`  
Output: `[[1,1],[1,1]]`

**Constraints:**
- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 25`
- `board[i][j]` is `0` or `1`

**Follow-up:**  
Can you solve it in-place, ensuring all cells are updated simultaneously? How would you handle the infinite board scenario when live cells reach the border?

## Code Template

```python
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach creates a copy of the board to preserve the current state while updating cells. It counts live neighbors for each cell and applies the Game of Life rules to determine the next state. The time complexity is O(mn) and space complexity is O(mn).
- [Solution 2](./solution_02.md): This approach updates the board in-place using special markers to encode state transitions without extra space. It counts live neighbors using absolute values to handle intermediate states and updates the board accordingly. The time complexity is O(mn) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
