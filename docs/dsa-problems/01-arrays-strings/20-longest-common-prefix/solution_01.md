# Intuition

To find the longest common prefix among a list of strings, compare characters at each position across all strings. Stop when a mismatch is found or the shortest string ends.

# Approach

1. Find the minimum length among all strings, since the common prefix cannot be longer than the shortest string.
2. For each character position up to the minimum length, check if all strings have the same character.
3. If a mismatch is found, return the prefix up to that point. If no mismatch, return the prefix of minimum length.

# Complexity

- Time complexity:
$$O(N \cdot M)$$, where $N$ is the number of strings and $M$ is the length of the shortest string.

- Space complexity:
$$O(1)$$, ignoring the output string.

# Code

```python
from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        min_len = len(strs[0])
        for st in strs[1:]:
            min_len = min(min_len, len(st))

        ans = ""
        for i in range(min_len):
            ch = strs[0][i]
            ch_diff = False
            for st in strs[1:]:
                if st[i] != ch:
                    ch_diff = True
                    break
            if ch_diff:
                break
            else:
                ans += ch

        return ans
```

[Back to Problem Statement](./index.md)
