# Minimum Window Substring

## Problem Statement

Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `""`.

The test cases will be generated such that the answer is unique.

**Examples**

**Example 1:**
- Input: `s = "ADOBECODEBANC"`, `t = "ABC"`
- Output: `"BANC"`
- Explanation: The minimum window substring `"BANC"` includes `'A'`, `'B'`, and `'C'` from string `t`.

**Example 2:**
- Input: `s = "a"`, `t = "a"`
- Output: `"a"`
- Explanation: The entire string `s` is the minimum window.

**Example 3:**
- Input: `s = "a"`, `t = "aa"`
- Output: `""`
- Explanation: Both `'a'`s from `t` must be included in the window. Since the largest window of `s` only has one `'a'`, return empty string.

**Constraints**
- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.

## Code Template

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses a sliding window technique with two pointers and a hash map to count character frequencies. The time complexity is O(m + n) and space complexity is O(m + n).
- [Solution 2](./solution_02.md): This optimized approach filters the string `s` to only include characters present in `t`, reducing the number of iterations needed. It also uses a sliding window technique with two pointers and a hash map. The time complexity is O(m + n) and space complexity is O(m + n).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
