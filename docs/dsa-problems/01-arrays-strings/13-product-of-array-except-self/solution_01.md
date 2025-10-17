# Intuition

To solve this problem, we need to compute the product of all elements except the current one for each index, without using division. The first thought is to use prefix and suffix products: for each index, multiply the product of all elements before it (prefix) and after it (suffix).

# Approach

We use two passes:
- First, compute prefix products for each index (product of all elements to the left).
- Second, compute suffix products for each index (product of all elements to the right).
- Finally, for each index, multiply its prefix and suffix product to get the answer.

This approach avoids division and ensures each element's product excludes itself. The code uses extra arrays for prefix and suffix, but this can be optimized to use only the output array for $$O(1)$$ extra space (excluding output).

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$ (for prefix and suffix arrays; can be optimized to $$O(1)$$ extra space)

# Code

```python
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        prefix_prod = [0] * n
        suffix_prod = [0] * n
        answer = []

        # prefix_prod[i] is the product of all elements before i
        prefix_prod[0] = 1
        for i in range(1, n):
            prefix_prod[i] = prefix_prod[i - 1] * nums[i - 1]

        # suffix_prod[i] is the product of all elements after i
        suffix_prod[n - 1] = 1
        for i in range(n - 2, -1, -1):
            suffix_prod[i] = suffix_prod[i + 1] * nums[i + 1]

        # answer[i] = prefix_prod[i] * suffix_prod[i]
        for i in range(n):
            answer.append(prefix_prod[i] * suffix_prod[i])

        return answer
```

[Back to Problem Statement](./index.md)
