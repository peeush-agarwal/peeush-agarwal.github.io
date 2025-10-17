# Intuition

To find the first occurrence of `needle` in `haystack`, we can check every possible starting position in `haystack` and compare the substring with `needle`. If a match is found, return the starting index; otherwise, return -1.

# Approach

We iterate through `haystack` from index 0 to `n - m` (where `n` is the length of `haystack` and `m` is the length of `needle`). For each position, we compare the substring of length `m` with `needle`. If all characters match, we return the current index. If no match is found after checking all positions, we return -1.

# Complexity

- Time complexity:
$$O((n - m + 1) \cdot m)$$

- Space complexity:
$$O(1)$$

# Code

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        m = len(needle)
        n = len(haystack)

        if n < m:
            return -1

        for i in range(n - m + 1):
            for j in range(m):
                if needle[j] != haystack[i + j]:
                    break

                if j == m - 1:
                    return i

        return -1
```

[Back to Problem Statement](./index.md)
