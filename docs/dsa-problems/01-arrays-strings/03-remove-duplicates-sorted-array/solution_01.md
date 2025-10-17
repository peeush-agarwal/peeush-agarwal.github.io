# Intuition

The array is already sorted, so all duplicates are adjacent. We can use this property to efficiently remove duplicates in-place by overwriting them as we iterate through the array.

# Approach

We use a two-pointer technique:
- One pointer (`insert_index`) keeps track of the position where the next unique element should be placed.
- The other pointer (`i`) iterates through the array.
- For each element, if it is different from the previous element, we place it at the `insert_index` and increment `insert_index`.
- At the end, `insert_index` will be the count of unique elements.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)

        if n == 0:
            return 0
        
        insert_index = 1  # Position to insert the next unique element
        for i in range(1, n):
            # If current element is not equal to the previous, it's unique
            if nums[i] != nums[i-1]:
                nums[insert_index] = nums[i]  # Place unique element
                insert_index += 1  # Move to next position
        
        return insert_index  # Number of unique elements
```

[Back to Problem Statement](./index.md)
