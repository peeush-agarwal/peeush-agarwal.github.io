# Two Sum

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

- Each input will have exactly one solution.
- You may not use the same element twice.
- The answer can be returned in any order.

### Examples

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums[0] + nums[1] == 9, so return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**
```
Input: nums = [3,3], target = 6
Output: [0,1]
```

### Constraints

- 2 <= nums.length <= 10⁴
- -10⁹ <= nums[i] <= 10⁹
- -10⁹ <= target <= 10⁹
- Only one valid answer exists.

### Follow-up

Can you come up with an algorithm that has less than O(n²) time complexity?

## Code Template

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md) - Using a hash map to store previously seen numbers and their indices. Time complexity: O(n), Space complexity: O(n).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
