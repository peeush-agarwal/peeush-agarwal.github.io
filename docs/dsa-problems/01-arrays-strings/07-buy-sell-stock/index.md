# Best time to buy and sell stock

## Problem Description

You are given an array `prices` where `prices[i]` represents the price of a given stock on the *i*-th day.

Your goal is to maximize your profit by choosing a single day to buy one stock and a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If no profit can be made, return `0`.

### Example 1

**Input:**  
`prices = [7,1,5,3,6,4]`  
**Output:**  
`5`  
**Explanation:**  
Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5.  
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

### Example 2

**Input:**  
`prices = [7,6,4,3,1]`  
**Output:**  
`0`  
**Explanation:**  
In this case, no transactions are done and the max profit = 0.

### Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

## Code Template

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](solution_01.md): This approach uses a brute-force method to check all possible pairs of buy and sell days to find the maximum profit.
- [Solution 2](solution_02.md): This approach optimizes the process by keeping track of the minimum price seen so far and calculating potential profits in a single pass through the array.

[Back to Problems List](../index.md) | [Back to Categories](../../index.md)
