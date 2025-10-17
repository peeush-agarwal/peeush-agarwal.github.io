# Intuition

To optimize the minimum window substring search, we can filter out irrelevant characters from `s` that are not present in `t`. This reduces the number of characters we need to process, making the sliding window more efficient.

# Approach

- Use a Counter to store the required counts of each character in `t`.
- Filter `s` to only include characters present in `t`, storing their indices and values.
- Use two pointers (`left` and `right`) to represent the current window in the filtered list.
- Expand the window by moving `right` and updating the counts of characters seen.
- When the window contains all required characters (with correct counts), try to contract it from the left to find the smallest valid window.
- Track the minimum window found during the process.
- Return the substring corresponding to the minimum window, or an empty string if no such window exists.

# Complexity

- Time complexity:
$$O(m + n)$$, where $m$ is the length of $s$ and $n$ is the length of $t$ (filtering and sliding window both run in linear time).

- Space complexity:
$$O(m + n)$$, for storing the filtered list and character counts.

# Code

```python
from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        dict_t = Counter(t)
        required = len(dict_t)

        filtered_s = []
        for i, char in enumerate(s):
            if char in dict_t:
                filtered_s.append((i, char))

        m = len(filtered_s)

        left, right = 0, 0
        formed = 0
        window_counts = defaultdict(int)
        ans = (float("inf"), left, right)

        for right in range(m):
            character = filtered_s[right][1]
            window_counts[character] += 1

            if window_counts[character] == dict_t[character]:
                formed += 1

            while left <= right and formed == required:
                character = filtered_s[left][1]

                end = filtered_s[right][0]
                start = filtered_s[left][0]
                if end - start + 1 < ans[0]:
                    ans = (end - start + 1, start, end)

                window_counts[character] -= 1
                if window_counts[character] < dict_t[character]:
                    formed -= 1

                left += 1

        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]
```

[Back to Problem Statement](./index.md)
