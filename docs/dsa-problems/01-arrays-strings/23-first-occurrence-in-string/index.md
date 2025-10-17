# Find the Index of the First Occurrence in a String

## Problem Statement

Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

### Examples

**Example 1:**
```
Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
```

**Example 2:**
```
Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.
```

### Constraints

- `1 <= haystack.length, needle.length <= 10^4`
- `haystack` and `needle` consist of only lowercase English characters.

## Code Template

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        # Your code here
        pass
```

## Solutions

- [Solution 1](solution_01.md): This approach checks every possible starting position in `haystack` and compares the substring with `needle`. It has a time complexity of O(n * m) and a space complexity of O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
