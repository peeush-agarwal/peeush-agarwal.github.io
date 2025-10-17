# Intuition

The key insight is that if we can complete the circuit, there must be a starting point where we never run out of gas. We can use a greedy approach: if at any point our current gas becomes negative, we know we cannot start from any previous station, so we reset and try starting from the next station.

# Approach

We use two variables to track our progress:
1. `total_gain`: Sum of all (gas[i] - cost[i]) to check if a solution exists
2. `curr_gain`: Current gas tank level as we traverse

We iterate through all stations:
- Add the net gain (gas[i] - cost[i]) to both totals
- If `curr_gain` becomes negative, we reset it to 0 and update our answer to the next station
- Finally, return the answer only if `total_gain >= 0` (solution exists)

The algorithm works because if we can't reach station j from station i, then we also can't reach station j from any station between i and j-1.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(1)$$

# Code

```python3
from typing import List

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        n = len(gas)

        total_gain = 0
        curr_gain = 0
        answer = 0

        for i in range(n):
            total_gain += gas[i] - cost[i]
            curr_gain += gas[i] - cost[i]

            if curr_gain < 0:
                curr_gain = 0
                answer = i + 1

        return answer if total_gain >= 0 else -1
```

[Back to Problem Statement](./index.md)
