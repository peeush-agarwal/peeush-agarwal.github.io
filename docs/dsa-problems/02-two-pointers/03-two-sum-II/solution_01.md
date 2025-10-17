# Intuition

Since the array is sorted, we can use the two-pointer technique to efficiently find two numbers that sum to the target. This avoids the need for nested loops and leverages the sorted property.

# Approach

Initialize two pointers: one at the start (`i`) and one at the end (`j`) of the array. Calculate the sum of the numbers at these pointers. If the sum equals the target, return their indices (1-based). If the sum is less than the target, increment the left pointer. If the sum is greater, decrement the right pointer. Repeat until the solution is found.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i, j = 0, len(numbers) - 1

        while i < j:
            sum_ = numbers[i] + numbers[j]
            if sum_ == target:
                return [i + 1, j + 1]
            elif sum_ < target:
                i += 1
            else:
                j -= 1

        raise Exception("No solution exists.")
```

[Back to Problem Statement](./index.md)
