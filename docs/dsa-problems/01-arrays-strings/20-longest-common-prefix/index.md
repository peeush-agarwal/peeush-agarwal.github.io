# Longest Common Prefix

## Problem Description

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

### Examples

**Example 1:**
```
Input: strs = ["flower","flow","flight"]
Output: "fl"
```

**Example 2:**
```
Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
```

### Constraints

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` consists of only lowercase English letters if it is non-empty.

## Code Template

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach compares characters at each position across all strings until a mismatch is found or the shortest string ends. It has a time complexity of O(N * M) and space complexity of O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
