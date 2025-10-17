# Intuition

To check if `s` is a subsequence of `t`, we can use two pointers: one for `s` and one for `t`. We move through `t`, and whenever we find a character that matches the current character in `s`, we advance the pointer for `s`. If we reach the end of `s`, it means all characters of `s` have been found in order in `t`.

# Approach

Initialize a pointer `j` for `s` at 0. Iterate through `t` with pointer `i`. If `t[i]` matches `s[j]`, increment `j`. If `j` reaches the length of `s`, return `True`. If the loop ends and `j` is less than the length of `s`, return `False`.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of `t`.

- Space complexity:
$$O(1)$$

# Code

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        m = len(s)
        n = len(t)

        if m == 0:
            return True
        elif n < m:
            return False

        j = 0
        for i in range(n):
            if s[j] == t[i]:
                j += 1

            if j == m:
                return True

        return j == m
```

[Back to Problem Statement](./index.md)
