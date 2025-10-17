# Intuition

To find the longest substring without repeating characters, we need to keep track of the last seen index of each character and use a sliding window to ensure all characters in the current window are unique.

# Approach

- Use an array to store the last seen index of each ASCII character.
- Use two pointers (`left` and `right`) to represent the current window.
- For each character, if it was seen in the current window, move `left` to one position after its last occurrence.
- Update the last seen index and the maximum length found.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the string (each character is processed once).

- Space complexity:
$$O(1)$$, since the array size is fixed (128 for ASCII).

# Code

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        chars_index = [-1] * 128
        left, right = 0, 0
        res = -float("inf")

        for right in range(len(s)):
            ch_ascii = ord(s[right])

            ch_index = chars_index[ch_ascii]

            while ch_index != -1 and (left <= ch_index <= right):
                left = ch_index + 1

            chars_index[ch_ascii] = right
            res = max(res, right - left + 1)

        return int(res if res >= 0 else 0)
```

[Back to Problem Statement](./index.md)
