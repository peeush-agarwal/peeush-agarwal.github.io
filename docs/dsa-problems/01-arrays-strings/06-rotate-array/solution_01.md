# Intuition

To rotate the array to the right by $k$ steps, we need to move each element to a new position. A naive approach would use extra space, but the problem asks for an in-place solution with $O(1)$ extra space.

# Approach

We use the **reverse method** to rotate the array in-place:
1. Reverse the entire array.
2. Reverse the first $k$ elements.
3. Reverse the remaining $n - k$ elements.

This works because reversing the whole array puts the elements that need to be at the front in the correct order after the subsequent reversals.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k %= n

        def reverse(start, end):
            i = start
            j = end
            while i < j:
                nums[i], nums[j-1] = nums[j-1], nums[i]
                i += 1
                j -= 1

        reverse(0, n)
        reverse(0, k)
        reverse(k, n)
```

[Back to Problem Statement](./index.md)
