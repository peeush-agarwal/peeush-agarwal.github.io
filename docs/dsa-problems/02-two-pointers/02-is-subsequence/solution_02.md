# Intuition

For a large number of queries, we need to optimize checking if each string `s` is a subsequence of `t`. Preprocessing `t` to quickly find the next occurrence of each character allows us to answer each query efficiently.

# Approach

We preprocess `t` by storing the indices of each character in a dictionary. For each character in `s`, we use binary search to find the next valid index in `t` that comes after the previous match. If we can match all characters of `s` in order, then `s` is a subsequence of `t`.

# Complexity

- Time complexity:
  - Preprocessing: $$O(n)$$
  - Each query: $$O(m \log n)$$, where $m$ is the length of `s` and $n$ is the length of `t`.

- Space complexity:
  - $$O(n)$$ for storing indices of each character in `t`.

# Code

```python
import bisect
from collections import defaultdict

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        letter_indices_table = defaultdict(list)
        for index, letter in enumerate(t):
            letter_indices_table[letter].append(index)

        curr_match_index = -1
        for letter in s:
            if letter not in letter_indices_table:
                return False  # no match at all, early exit

            # greedy match with binary search
            indices_list = letter_indices_table[letter]
            match_index = bisect.bisect_right(indices_list, curr_match_index)
            if match_index != len(indices_list):
                curr_match_index = indices_list[match_index]
            else:
                return False  # no suitable match found, early exit

        return True
```

[Back to Problem Statement](./index.md)
