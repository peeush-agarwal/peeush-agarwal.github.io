# Longest Substring Without Repeating Characters

## Problem Statement

Given a string `s`, determine the length of the longest substring that contains no repeating characters.

### Examples

**Example 1**  
Input: `s = "abcabcbb"`  
Output: `3`  
Explanation: The longest substring without repeating characters is `"abc"`, with a length of 3. Other valid substrings include `"bca"` and `"cab"`.

**Example 2**  
Input: `s = "bbbbb"`  
Output: `1`  
Explanation: The longest substring without repeating characters is `"b"`, with a length of 1.

**Example 3**  
Input: `s = "pwwkew"`  
Output: `3`  
Explanation: The longest substring without repeating characters is `"wke"`, with a length of 3. Note that `"pwke"` is a subsequence, not a substring.

### Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols, and spaces.

## Code Template

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses a sliding window technique with a set to track characters in the current substring. The time complexity is O(n) and space complexity is O(min(m, n)), where m is the size of the character set and n is the length of the string.

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
