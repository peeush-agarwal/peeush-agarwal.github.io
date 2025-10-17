# Intuition

To check if a string follows a given pattern, we need to ensure a bijection between pattern letters and words in the string. Each letter should map to a unique word, and each word should map to a unique letter.

# Approach

- Split the string into words and check if the number of words matches the pattern length.
- Use a dictionary to map pattern letters to words and a set to track mapped words.
- For each letter-word pair, check if the mapping is consistent and that no two letters map to the same word.
- If all checks pass, the string follows the pattern.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the pattern (each character and word is processed once).

- Space complexity:
$$O(n)$$, for the mapping and set.

# Code

```python
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        if len(pattern) != len(words):
            return False

        mapped_dict = {}
        mapped_set = set()

        for p, word in zip(pattern, words):
            mapped_dict[p] = mapped_dict.get(p, word)
            if mapped_dict[p] != word:
                return False

            mapped_set.add(word)

        if len(mapped_set) != len(mapped_dict):
            return False
        return True
```

[Back to Problem Statement](./index.md)
