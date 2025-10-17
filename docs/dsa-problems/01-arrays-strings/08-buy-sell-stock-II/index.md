# Buy and Sell Stock II

## Problem Description

You are given an integer array `prices` where `prices[i]` represents the price of a given stock on the *i*-th day.

On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you are allowed to sell and buy the stock multiple times on the same day, as long as you never hold more than one share at any time.

Your task is to find and return the **maximum profit** you can achieve.

---

### Examples

**Example 1:**

```
Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation: 
Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.
```

**Example 2:**

```
Input: prices = [1,2,3,4,5]
Output: 4
Explanation: 
Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
Total profit is 4.
```

**Example 3:**

```
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: 
There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.
```

---

### Constraints

- `1 <= prices.length <= 3 * 10^4`
- `0 <= prices[i] <= 10^4`

## Code Template

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](solution_01.md) - This approach tracks local minima and maxima to capture all profit segments. The time complexity is O(n) and space complexity is O(1).
- [Solution 2](solution_02.md) - This approach sums all positive price differences between consecutive days. The time complexity is O(n) and space complexity is O(1).

[Back to Problems List](../index.md) | [Back to Categories](../../index.md)
