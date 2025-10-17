# Valid Anagram

## Problem Statement

Given two strings `s` and `t`, determine if `t` is an anagram of `s`. Return `true` if it is, otherwise return `false`.

### Examples

**Example 1:**
```
Input: s = "anagram", t = "nagaram"
Output: true
```

**Example 2:**
```
Input: s = "rat", t = "car"
Output: false
```

### Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

### Follow Up

How would you adapt your solution if the inputs contain Unicode characters?

## Code Template

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md) - Using Counter to count character frequencies. Time complexity: O(n), Space complexity: O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
