# Ransom Note

## Problem Statement

Given two strings `ransomNote` and `magazine`, determine if `ransomNote` can be constructed using the letters from `magazine`. Each letter in `magazine` can only be used once in constructing `ransomNote`.

### Examples

**Example 1**  
Input: `ransomNote = "a"`, `magazine = "b"`  
Output: `false`

**Example 2**  
Input: `ransomNote = "aa"`, `magazine = "ab"`  
Output: `false`

**Example 3**  
Input: `ransomNote = "aa"`, `magazine = "aab"`  
Output: `true`

### Constraints

- `1 <= ransomNote.length, magazine.length <= 10^5`
- Both `ransomNote` and `magazine` consist of lowercase English letters.

## Code Template

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach counts the frequency of each letter in the magazine using a dictionary. It then checks if each letter in the ransom note can be constructed from the magazine's letters by decrementing the count. The time complexity is O(m + n) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
