# Is Subsequence

## Problem Statement

Given two strings `s` and `t`, determine if `s` is a subsequence of `t`. Return `true` if it is, otherwise return `false`.

A subsequence of a string is a new string formed from the original string by deleting some (possibly none) characters without changing the order of the remaining characters. For example, `"ace"` is a subsequence of `"abcde"`, but `"aec"` is not.

### Examples

**Example 1:**
```
Input: s = "abc", t = "ahbgdc"
Output: true
```

**Example 2:**
```
Input: s = "axc", t = "ahbgdc"
Output: false
```

### Constraints

- `0 <= s.length <= 100`
- `0 <= t.length <= 10^4`
- `s` and `t` consist only of lowercase English letters.

### Follow Up

Suppose there are a large number of incoming strings `s1, s2, ..., sk` where `k >= 10^9`, and you want to check for each if `t` contains it as a subsequence. How would you optimize your approach for this scenario?

## Code Template

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # Your code here
        pass
```

## Solutions

- [Solution 1](solution_01.md): This approach uses two pointers to check if `s` is a subsequence of `t`. It has a time complexity of O(n) and a space complexity of O(1).
- [Solution 2](solution_02.md): This approach preprocesses `t` to allow for efficient checking of multiple `s` strings using binary search. It has a preprocessing time complexity of O(n) and each query takes O(m log n), where m is the length of `s` and n is the length of `t`. The space complexity is O(n).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
