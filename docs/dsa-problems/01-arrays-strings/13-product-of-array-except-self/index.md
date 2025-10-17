# Product of Array Except Self

## Problem Description

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.
- You must write an algorithm that runs in $$O(n)$$ time and **without using the division operation**.

### Example 1

**Input:** `nums = [1,2,3,4]`  
**Output:** `[24,12,8,6]`

### Example 2

**Input:** `nums = [-1,1,0,-3,3]`  
**Output:** `[0,0,9,0,0]`

### Constraints

- $$2 \leq \text{nums.length} \leq 10^5$$
- $$-30 \leq \text{nums}[i] \leq 30$$
- The input is generated such that `answer[i]` is guaranteed to fit in a 32-bit integer.

### Follow Up

Can you solve the problem in $$O(1)$$ extra space complexity? (The output array does not count as extra space for space complexity analysis.)

## Code Template

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](solution_01.md) - This approach uses prefix and suffix products to compute the result in $$O(n)$$ time and $$O(n)$$ space. It can be optimized to use $$O(1)$$ extra space.
- [Solution 2](solution_02.md) - This approach optimizes space usage by using the output array to store prefix products and a single variable for suffix products, achieving $$O(1)$$ extra space.

[Back to Problems List](../index.md) | [Back to Categories](../../index.md)
