# Intuition

Instead of simulating the zigzag traversal, I thought about how the characters are positioned in each row. By analyzing the pattern, I realized that the characters for each row can be picked directly using calculated indices, which avoids the need for extra direction tracking.

# Approach

- If `numRows` is 1 or the string length is less than or equal to `numRows`, return the string as is.
- For each row, iterate through the string and pick characters at calculated intervals:
    - The interval between vertical characters is `2 * numRows - 2`.
    - For middle rows, there is an additional character between the verticals, which can be calculated using the current row index.
- Collect all characters in order and join them to form the result.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$

# Code

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        n = len(s)
        if (numRows == 1) or (n <= numRows):
            return s

        ans = []
        chars_in_section = 2 * numRows - 2

        for i in range(numRows):
            index = i
            while index < n:
                ans.append(s[index])

                if (i != 0) and (i != numRows - 1):
                    chars_in_betw = chars_in_section - 2 * i
                    second_index = index + chars_in_betw

                    if second_index < n:
                        ans.append(s[second_index])

                index += chars_in_section

        return "".join(ans)
```

[Back to Problem Statement](./index.md)
