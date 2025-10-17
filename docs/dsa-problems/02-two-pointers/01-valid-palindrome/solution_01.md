# Intuition

To check if a string is a palindrome, we need to ignore non-alphanumeric characters and compare the string from both ends, considering only lowercase letters and digits.

# Approach

- Use two pointers, one starting from the beginning and one from the end of the string.
- Move the pointers inward, skipping non-alphanumeric characters.
- Compare the characters at both pointers (after converting to lowercase).
- If all corresponding characters match, the string is a palindrome; otherwise, it is not.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the string (each character is checked at most once).

- Space complexity:
$$O(1)$$, since no extra space is used except for variables.

# Code

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        i, j = 0, len(s) - 1

        while i < j:
            while i < j and not s[i].isalnum():
                i += 1
            while i < j and not s[j].isalnum():
                j -= 1

            if s[i].lower() != s[j].lower():
                return False

            i += 1
            j -= 1

        return True
```

[Back to Problem Statement](./index.md)
