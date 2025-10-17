# Intuition

To find the length of the last word in a string, we can scan the string from the end, skipping any trailing spaces, and then count the characters until we hit another space or the start of the string.

# Approach

- Start from the end of the string and move backwards.
- Skip all trailing spaces.
- Once a non-space character is found, start counting until a space is encountered or the start of the string is reached.
- The count gives the length of the last word.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the string (since we may scan the entire string).

- Space complexity:
$$O(1)$$ (no extra space used except variables).

# Code

```python
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        n = len(s)

        ans = 0
        first_char = None
        for i in range(n - 1, -1, -1):
            c = s[i]
            if c == " " and first_char is not None:
                break
            elif c != " ":
                ans += 1
                first_char = first_char or c

        return ans
```

[Back to Problem Statement](./index.md)
