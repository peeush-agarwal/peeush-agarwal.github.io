# Intuition

The follow-up asks for $$O(1)$$ extra space (excluding the output array). The intuition is to use the output array itself to store prefix products, and then multiply by the running suffix product in a second pass, thus avoiding extra arrays.

# Approach

- First pass: Fill the output array (`answer`) with prefix products (product of all elements to the left of each index).
- Second pass: Traverse from right to left, maintaining a running product (`R`) of all elements to the right, and multiply it into the output array.
- This way, for each index, the output is the product of all elements except itself, using only the output array and a single variable for suffix product.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$ (excluding the output array)

# Code

```python
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [0] * n
        R = 1

        # answer[i] will contain the product of all elements to the left of i
        answer[0] = 1
        for i in range(1, n):
            answer[i] = answer[i - 1] * nums[i - 1]

        # R is the running product of all elements to the right of i
        for i in range(n - 1, -1, -1):
            answer[i] = answer[i] * R
            R *= nums[i]

        return answer
```

[Back to Problem Statement](./index.md)
