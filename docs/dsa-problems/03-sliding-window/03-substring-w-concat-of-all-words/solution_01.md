# Intuition

To find all starting indices of substrings that are concatenations of all words, we need to check every possible window of the correct length and verify if it contains all words exactly once. Since all words have the same length, we can use a sliding window approach with multiple starting offsets.

# Approach

- Calculate the total length of the concatenated substring (`substring_size = len(words) * len(words[0])`).
- Use a Counter to store the required frequency of each word.
- For each possible offset (from 0 to `word_len - 1`), use a sliding window to check substrings:
    - Move the window in steps of `word_len`.
    - Track the words seen and their counts.
    - If a word is not in the required list or is seen too many times, reset the window.
    - If all words are matched exactly, record the starting index.

# Complexity

- Time complexity:
$$O(N \cdot k)$$, where $N$ is the length of $s$ and $k$ is the number of words (each window is checked, and each word in the window is processed).

- Space complexity:
$$O(k)$$, for storing word counts and the sliding window state.

# Code

```python
from collections import Counter, defaultdict
from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        n = len(s)
        k = len(words)
        word_len = len(words[0])
        substring_size = k * word_len
        words_count = Counter(words)

        def sliding_window(left):
            seen = defaultdict(int)
            words_remaining = k
            excess_word = False

            for right in range(left, n, word_len):
                sub = s[right : right + word_len]
                if sub not in words_count:
                    seen = defaultdict(int)
                    words_remaining = k
                    excess_word = False
                    left = right + word_len
                else:
                    while right - left == substring_size or excess_word:
                        leftmost_word = s[left : left + word_len]
                        left += word_len
                        seen[leftmost_word] -= 1

                        if seen[leftmost_word] == words_count[leftmost_word]:
                            excess_word = False
                        else:
                            words_remaining += 1

                    seen[sub] += 1
                    if seen[sub] <= words_count[sub]:
                        words_remaining -= 1
                    else:
                        excess_word = True

                    if words_remaining == 0 and not excess_word:
                        ans.append(left)

        ans = []
        for i in range(word_len):
            sliding_window(i)

        return ans
```

[Back to Problem Statement](./index.md)
