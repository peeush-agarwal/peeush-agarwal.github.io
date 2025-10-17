# Intuition

The problem requires merging two sorted arrays into one, in-place, using the extra space at the end of `nums1`. My first thought is to avoid overwriting useful data in `nums1` by starting the merge from the end of the array, filling in the largest elements first.

# Approach

We use three pointers:
- `i` points to the last valid element in `nums1` (index `m-1`).
- `j` points to the last element in `nums2` (index `n-1`).
- `k` points to the last position in `nums1` (index `m+n-1`).

We compare `nums1[i]` and `nums2[j]` and place the larger one at `nums1[k]`, then move the corresponding pointer backward. We repeat this until either array is exhausted. If any elements remain in `nums2`, we copy them to the front of `nums1`.

# Complexity

- Time complexity:
$$O(m + n)$$

- Space complexity:
$$O(1)$$

# Code

```python
from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i, j, k = m - 1, n - 1, m + n - 1
        # Merge from the end
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
        # If any elements left in nums2, copy them
        while j >= 0:
            nums1[k] = nums2[j]
            j -= 1
            k -= 1
```

[Back to Problem Statement](./index.md)
