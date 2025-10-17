# Intuition

The problem asks for all unique triplets in the array that sum to zero. My first thought is to use a hash set to avoid duplicates and a hash map to efficiently check for the required complement for each pair.

# Approach

Iterate through the array, treating each element as the first element of a potential triplet. For each first element, use a hash map to track the required complement for the remaining two elements. To avoid duplicate triplets, use a set to store already processed first elements and another set to store the resulting triplets as sorted tuples. Finally, convert the set of tuples to a list of lists for the result.

# Complexity

- Time complexity:
$$O(n^2)$$

- Space complexity:
$$O(n)$$

# Code

```python
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res, dups = set(), set()
        seen = {}

        for i in range(len(nums)):
            if nums[i] not in dups:
                dups.add(nums[i])

                for j in range(i + 1, len(nums)):
                    compl = -nums[i] - nums[j]
                    if compl in seen and seen[compl] == i:
                        res.add(tuple(sorted((nums[i], nums[j], compl))))
                    seen[nums[j]] = i

        return [list(x) for x in res]
```

[Back to Problem Statement](./index.md)
