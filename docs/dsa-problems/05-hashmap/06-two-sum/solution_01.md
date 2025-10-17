# Intuition

To find two numbers that add up to the target, we can use a hash map to store previously seen numbers and their indices. For each number, we check if its complement (target - current number) exists in the map.

# Approach

- Iterate through the array, for each number:
    - Compute its complement with respect to the target.
    - If the complement is in the map, return the indices.
    - Otherwise, store the current number and its index in the map.
- This ensures each number is checked only once and the solution is found in linear time.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the array (each element is processed once).

- Space complexity:
$$O(n)$$, for storing the hash map.

# Code

```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map_ = {nums[0]: 0}

        for i in range(1, len(nums)):
            comp = target - nums[i]

            if comp in map_:
                return [map_[comp], i]

            map_[nums[i]] = i

        return [-1, -1]
```

[Back to Problem Statement](./index.md)
