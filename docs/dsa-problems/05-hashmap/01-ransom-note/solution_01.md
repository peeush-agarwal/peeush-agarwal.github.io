# Intuition

To check if the ransom note can be constructed from the magazine, we need to ensure that every letter in the ransom note appears at least as many times in the magazine.

# Approach

- Count the frequency of each letter in the magazine using a dictionary.
- For each letter in the ransom note, check if it exists in the magazine's count and has a positive count.
- If so, decrement the count; otherwise, return `False`.
- If all letters are accounted for, return `True`.

# Complexity

- Time complexity:
$$O(m + n)$$, where $m$ and $n$ are the lengths of `magazine` and `ransomNote`.

- Space complexity:
$$O(1)$$ (since the alphabet size is fixed at 26, the dictionary size is bounded).

# Code

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        m_counts = {}
        for c in magazine:
            m_counts[c] = m_counts.get(c, 0) + 1

        for c in ransomNote:
            if c not in m_counts or m_counts[c] == 0:
                return False

            m_counts[c] -= 1

        return True
```

[Back to Problem Statement](./index.md)
