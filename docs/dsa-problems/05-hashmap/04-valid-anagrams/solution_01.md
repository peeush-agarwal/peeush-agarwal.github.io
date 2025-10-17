# Intuition

To check if two strings are anagrams, we need to verify that both strings contain the same characters with the same frequencies.

# Approach

- Use a Counter to count the frequency of each character in `t`.
- For each character in `s`, decrement its count in the Counter.
- After processing, check if all counts in the Counter are zero.
- If so, the strings are anagrams; otherwise, they are not.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the strings (each character is processed once).

- Space complexity:
$$O(1)$$ (since the alphabet size is fixed at 26 for lowercase English letters).

# Code

```python
from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        t_count = Counter(t)
        for c in s:
            if c in t_count:
                t_count[c] -= 1

        for k, v in t_count.items():
            if v != 0:
                return False

        return True
```

[Back to Problem Statement](./index.md)
