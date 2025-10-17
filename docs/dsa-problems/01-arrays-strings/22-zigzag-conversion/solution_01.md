# Intuition

To solve the ZigZag conversion problem, I first thought about simulating the process of writing the string in a zigzag pattern row by row. The main challenge is to determine the direction of traversal (down or up) and to collect characters for each row accordingly.

# Approach

- If `numRows` is 1 or the string length is less than or equal to `numRows`, the zigzag pattern is just the string itself.
- Use a dictionary to represent each row, where the key is the row index and the value is a list of characters for that row.
- Iterate through the string, appending each character to the current row.
- Change direction (down or up) when reaching the top or bottom row by flipping the step variable.
- After processing all characters, concatenate the rows in order to get the final result.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$

# Code

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if (numRows == 1) or (len(s) <= numRows):
            return s

        rows = {}
        cur_row = 0
        step = 1

        for c in s:
            rows[cur_row] = rows.get(cur_row, [])
            rows[cur_row].append(c)
            cur_row += step

            if (cur_row <= 0) or (cur_row >= numRows - 1):
                step = -1 * step

        ans = []
        for r in range(numRows):
            ans.extend(rows[r])

        return "".join(ans)
```

[Back to Problem Statement](./index.md)
