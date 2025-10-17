# Length of Last Word

## Problem Statement

Given a string `s` consisting of words and spaces, return the length of the last word in the string.

A word is defined as a maximal substring consisting of non-space characters only.

### Examples

**Example 1:**
```
Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.
```

**Example 2:**
```
Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.
```

**Example 3:**
```
Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.
```

### Constraints

- `1 <= s.length <= 10^4`
- `s` consists of only English letters and spaces `' '`.
- There will be at least one word in `s`.

## Code Template

```python
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach scans the string from the end, skipping trailing spaces and counting characters until a space or the start of the string is reached. The time complexity is O(n) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
