# Group Anagrams

## Problem Statement

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

### Examples

**Example 1:**
```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```
**Explanation:**  
- "bat" has no anagrams in the list.  
- "nat" and "tan" are anagrams of each other.  
- "ate", "eat", and "tea" are anagrams of each other.

**Example 2:**
```
Input: strs = [""]
Output: [[""]]
```

**Example 3:**
```
Input: strs = ["a"]
Output: [["a"]]
```

### Constraints

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.

## Code Template

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md) - Using character count as a signature to group anagrams. Time complexity: O(N * K), Space complexity: O(N * K).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
