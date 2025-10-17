# Word Pattern

## Problem Statement

Given a pattern and a string `s`, determine if `s` follows the same pattern.

A string `s` follows a pattern if there is a bijection between each letter in the pattern and a non-empty word in `s`. This means:

- Each letter in the pattern maps to exactly one unique word in `s`.
- Each unique word in `s` maps to exactly one letter in the pattern.
- No two letters map to the same word, and no two words map to the same letter.

### Examples

**Example 1**

- Input: `pattern = "abba"`, `s = "dog cat cat dog"`
- Output: `true`
- Explanation:  
    - 'a' maps to "dog"  
    - 'b' maps to "cat"

**Example 2**

- Input: `pattern = "abba"`, `s = "dog cat cat fish"`
- Output: `false`

**Example 3**

- Input: `pattern = "aaaa"`, `s = "dog cat cat dog"`
- Output: `false`

### Constraints

- `1 <= pattern.length <= 300`
- `pattern` contains only lowercase English letters.
- `1 <= s.length <= 3000`
- `s` contains only lowercase English letters and spaces `' '`.
- `s` does not contain any leading or trailing spaces.
- All words in `s` are separated by a single space.

## Code Template

```python
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses a dictionary to map pattern letters to words and a set to track already mapped words. The time complexity is O(n) and space complexity is O(n).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
