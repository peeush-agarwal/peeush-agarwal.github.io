# Intuition

The h-index is the largest number h such that the researcher has at least h papers with at least h citations each. My first thought was to count, for each possible h, how many papers have at least h citations, and find the largest such h.

# Approach

We use a counting array `papers` where `papers[i]` counts the number of papers with exactly i citations (capped at n). We then iterate from the highest possible h down to 0, maintaining a cumulative sum of papers with at least h citations. The first h where this cumulative sum is at least h is the answer.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$

# Code

```python3
from typing import List

class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        papers = [0] * (n + 1)

        for i in range(n):
            papers[min(n, citations[i])] += 1

        cumm_papers = 0
        for h in range(n, -1, -1):
            cumm_papers += papers[h]
            if cumm_papers >= h:
                return h

        return 0
```

[Back to Problem Statement](./index.md)
