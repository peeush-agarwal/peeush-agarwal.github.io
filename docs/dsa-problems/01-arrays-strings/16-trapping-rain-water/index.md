# Trapping Rain Water

## Problem Description

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Example 1

```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```
**Explanation:**  
The above elevation map (black section) is represented by the array `[0,1,0,2,1,0,1,3,2,1,2,1]`. In this case, 6 units of rain water (blue section) are being trapped.

### Example 2

```
Input: height = [4,2,0,3,2,5]
Output: 9
```

### Constraints

- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

## Code Template

```python3
class Solution:
    def trap(self, height: List[int]) -> int:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](solution_01.md): This approach uses precomputed arrays to store the maximum heights to the left and right of each position. It has a time complexity of O(n) and a space complexity of O(n).
- [Solution 2](solution_02.md): This approach uses two pointers to optimize space usage. It has a time complexity of O(n) and a space complexity of O(1).

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
