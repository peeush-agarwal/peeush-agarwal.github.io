# Intuition

To reverse the words in a string, my first thought was to split the string into words, reverse their order, and join them back with a single space. However, since the problem asks to handle extra spaces and not use built-in split, I decided to manually parse the string and collect words.

# Approach

Iterate through the string character by character, building each word as a list of characters. When a space is encountered and a word has been built, join the word and add it to the answer list. After the loop, add any remaining word. Finally, reverse the list of words and join them with a single space.

# Complexity

- Time complexity:
$$O(n)$$

- Space complexity:
$$O(n)$$

# Code

```python
class Solution:
    def reverseWords(self, s: str) -> str:
        ans = []
        w = []
        i = 0
        while i < len(s):
            if s[i] != " ":
                w.append(s[i])
            elif w:
                w = "".join(w)
                ans.append(w)
                w = []

            i += 1

        if w:
            w = "".join(w)
            ans.append(w)
            w = []

        return " ".join(reversed(ans))
```

[Back to Problem Statement](./index.md)
