# Substring with Concatenation of All Words

## Problem Statement

Given a string `s` and an array of strings `words`, where all strings in `words` have the same length, find all starting indices of substrings in `s` that are a concatenation of each word in `words` exactly once and without any intervening characters. The order of words in the concatenation can be any permutation.

A valid concatenated substring contains all the words from `words` in any order, joined together. For example, if `words = ["ab", "cd", "ef"]`, then `"abcdef"`, `"abefcd"`, `"cdabef"`, `"cdefab"`, `"efabcd"`, and `"efcdab"` are valid concatenated strings. `"acdbef"` is not valid because it does not use all words in a permutation.

Return an array of all starting indices of such substrings in `s`. The answer can be in any order.

### Examples

**Example 1:**
```
Input: s = "barfoothefoobarman", words = ["foo","bar"]
Output: [0,9]
Explanation:
- Substring at index 0: "barfoo" is a concatenation of ["bar","foo"].
- Substring at index 9: "foobar" is a concatenation of ["foo","bar"].
```

**Example 2:**
```
Input: s = "wordgoodgoodgoodbestword", words = ["word","good","best","word"]
Output: []
Explanation:
- No valid concatenated substring found.
```

**Example 3:**
```
Input: s = "barfoofoobarthefoobarman", words = ["bar","foo","the"]
Output: [6,9,12]
Explanation:
- Substring at index 6: "foobarthe" is a concatenation of ["foo","bar","the"].
- Substring at index 9: "barthefoo" is a concatenation of ["bar","the","foo"].
- Substring at index 12: "thefoobar" is a concatenation of ["the","foo","bar"].
```

### Constraints

- `1 <= s.length <= 10^4`
- `1 <= words.length <= 5000`
- `1 <= words[i].length <= 30`
- `s` and `words[i]` consist of lowercase English letters.

## Code Template

```python
class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses a sliding window technique combined with a hash map to count occurrences of words. The time complexity is O(n * m) where n is the length of the string and m is the number of words, and space complexity is O(m).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
