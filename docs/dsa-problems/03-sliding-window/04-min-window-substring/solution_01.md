# Intuition

To find the minimum window substring containing all characters of `t`, we need to efficiently track the counts of required characters and use a sliding window to expand and contract the window as needed.

# Approach

- Use a Counter to store the required counts of each character in `t`.
- Use two pointers (`left` and `right`) to represent the current window in `s`.
- Expand the window by moving `right` and updating the counts of characters seen.
- When the window contains all required characters (with correct counts), try to contract it from the left to find the smallest valid window.
- Track the minimum window found during the process.
- Return the substring corresponding to the minimum window, or an empty string if no such window exists.

# Complexity

- Time complexity:
$$O(m + n)$$, where $m$ is the length of $s$ and $n$ is the length of $t$ (each character is processed at most twice).

- Space complexity:
$$O(n)$$, for storing character counts.

# Code

```python
from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        m = len(s)

        dict_t = Counter(t)
        required = len(dict_t)

        left, right = 0, 0
        formed = 0
        window_counts = defaultdict(int)
        ans = (float("inf"), left, right)

        for right in range(m):
            character = s[right]
            window_counts[character] += 1

            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1

            while left <= right and formed == required:
                character = s[left]

                if right - left + 1 < ans[0]:
                    ans = (right - left + 1, left, right)

                window_counts[character] -= 1
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1

                left += 1

        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]
```

[Back to Problem Statement](./index.md)
