# Intuition

To find the minimal length of a contiguous subarray with sum at least `target`, we can use prefix sums and binary search. For each starting index, we search for the smallest ending index such that the subarray sum is at least `target`.

# Approach

- Compute prefix sums for the array.
- For each possible starting index, use binary search to find the minimal ending index where the subarray sum is at least `target`.
- Track the minimal length found.
- If no such subarray exists, return 0.

# Complexity

- Time complexity:
$$O(n \log n)$$ (for each index, binary search is used)

- Space complexity:
$$O(n)$$ (for the prefix sum array)

# Code

```python
from typing import List

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        prefix_sum = [0] * n
        prefix_sum[0] = nums[0]

        for i in range(1, n):
            prefix_sum[i] = prefix_sum[i - 1] + nums[i]

        res = float("inf")
        for i in range(n):
            start, end = 0, n - 1
            while start <= end:
                mid = (start + end) // 2
                sub_sum = prefix_sum[mid] - prefix_sum[i] + nums[i]
                if sub_sum >= target:
                    res = min(res, mid - i + 1)
                    end = mid - 1
                else:
                    start = mid + 1

        return int(0 if res > n else res)
```

[Back to Problem Statement](./index.md)
