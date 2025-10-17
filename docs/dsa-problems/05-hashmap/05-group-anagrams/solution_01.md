# Intuition

To group anagrams, we need a way to identify strings that are anagrams of each other. Counting the frequency of each character provides a unique signature for each group of anagrams.

# Approach

- For each string, count the frequency of each letter (using a list of size 26).
- Use the tuple of counts as a key in a dictionary to group strings with the same signature.
- Return the grouped values as the result.

# Complexity

- Time complexity:
$$O(N \cdot K)$$, where $N$ is the number of strings and $K$ is the average length of each string (each character is processed once).

- Space complexity:
$$O(N \cdot K)$$, for storing the groups and character counts.

# Code

```python
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict

        ans = defaultdict(list)

        for s in strs:
            cnt = [0] * 26
            for c in s:
                cnt[ord(c) - ord("a")] += 1

            ans[tuple(cnt)].append(s)

        return list(ans.values())
```

[Back to Problem Statement](./index.md)
