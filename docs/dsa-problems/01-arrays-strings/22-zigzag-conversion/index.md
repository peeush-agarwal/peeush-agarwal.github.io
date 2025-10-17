# ZigZag conversion

## Problem Statement

Given a string, write it in a zigzag pattern on a given number of rows and then read the result line by line.

For example, the string `"PAYPALISHIRING"` written in a zigzag pattern with 3 rows looks like:

```
P   A   H   N
A P L S I I G
Y   I   R
```

Reading line by line gives: `"PAHNAPLSIIGYIR"`.

Implement the following function:

```python
def convert(s: str, numRows: int) -> str:
```

### Examples

**Example 1:**
- Input: `s = "PAYPALISHIRING"`, `numRows = 3`
- Output: `"PAHNAPLSIIGYIR"`

**Example 2:**
- Input: `s = "PAYPALISHIRING"`, `numRows = 4`
- Output: `"PINALSIGYAHRPI"`
- Explanation:
    ```
    P     I    N
    A   L S  I G
    Y A   H R
    P     I
    ```

**Example 3:**
- Input: `s = "A"`, `numRows = 1`
- Output: `"A"`

### Constraints

- `1 <= s.length <= 1000`
- `s` consists of English letters (lower-case and upper-case), `,` and `.`.
- `1 <= numRows <= 1000`

## Code Template

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This solution uses a list of strings to represent each row and simulates the zigzag pattern by iterating through the characters of the input string. It has a time complexity of O(n) and a space complexity of O(n).
- [Solution 2](./solution_02.md): This solution calculates the positions of characters in each row directly based on the zigzag pattern, avoiding the need for direction tracking. It also has a time complexity of O(n) and a space complexity of O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
