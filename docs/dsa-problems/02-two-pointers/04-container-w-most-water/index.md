# Container with most water

## Problem Statement

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the *i*-th line are `(i, 0)` and `(i, height[i])`.

Find two lines that, together with the x-axis, form a container such that the container contains the most water.

Return the maximum amount of water a container can store.

**Note:** You may not slant the container.

### Example 1

![img](./example_1_image.jpg)

**Input:** `height = [1,8,6,2,5,4,8,3,7]`  
**Output:** `49`  
**Explanation:** The above vertical lines are represented by array `[1,8,6,2,5,4,8,3,7]`. In this case, the max area of water (blue section) the container can contain is `49`.

### Example 2

**Input:** `height = [1,1]`  
**Output:** `1`

### Constraints

- `n == height.length`
- `2 <= n <= 10^5`
- `0 <= height[i] <= 10^4`

## Code Template

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses the two-pointer technique to find the maximum area in linear time. Time complexity is O(n) and space complexity is O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
