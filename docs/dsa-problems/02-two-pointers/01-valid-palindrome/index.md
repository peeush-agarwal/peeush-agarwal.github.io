# Valid Palindrome

## Problem Statement

A phrase is considered a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forwards and backwards. Alphanumeric characters include both letters and numbers.

Given a string `s`, determine whether it is a palindrome. Return `true` if it is a palindrome, and `false` otherwise.

### Examples

**Example 1:**
- Input: `s = "A man, a plan, a canal: Panama"`
- Output: `true`
- Explanation: After processing, `"amanaplanacanalpanama"` is a palindrome.

**Example 2:**
- Input: `s = "race a car"`
- Output: `false`
- Explanation: After processing, `"raceacar"` is not a palindrome.

**Example 3:**
- Input: `s = " "`
- Output: `true`
- Explanation: After removing non-alphanumeric characters, the string is empty `""`, which is considered a palindrome.

### Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

## Code Template

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses the two-pointer technique to compare characters from both ends of the string, skipping non-alphanumeric characters and ignoring case differences. The time complexity is O(n) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
