# Intuition

The problem requires distributing words into lines of a given width, then spacing them so each line is fully justified. The main challenge is distributing spaces evenly and handling special cases for the last line and lines with a single word.

# Approach

- Greedily pack as many words as possible into each line without exceeding `maxWidth`.
- For each line (except the last and lines with one word):
    - Calculate the number of spaces to distribute between words.
    - Distribute spaces as evenly as possible, with extra spaces assigned to the leftmost slots.
- For the last line and lines with a single word, left-justify and pad the end with spaces.
- Build each line and append to the result.

# Complexity

- Time complexity:
$$O(n . k)$$, where $n$ is the total number of words (each word is processed once) and $k$ is the maximum length of a line (which is at most `maxWidth`).

- Space complexity:
$$O(m)$$, for storing intermediate lines, where $m$ is the maximum width of the line.

# Code

```python
from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        def get_words(i):
            line = []
            line_len = 0

            while i < len(words) and line_len + len(words[i]) <= maxWidth:
                line.append(words[i])
                line_len += len(words[i]) + 1
                i += 1

            return line

        def build_line(line, i):
            total_len = -1
            for w in line:
                total_len += len(w) + 1

            extra_spaces = maxWidth - total_len

            if len(line) == 1 or i == len(words):
                return " ".join(line) + " " * extra_spaces

            word_count = len(line) - 1
            spaces_per_word = extra_spaces // word_count
            needs_extra_space = extra_spaces % word_count

            for j in range(needs_extra_space):
                line[j] += " "

            for j in range(word_count):
                line[j] += " " * spaces_per_word

            return " ".join(line)

        ans = []
        i = 0

        while i < len(words):
            line = get_words(i)
            i += len(line)
            ans.append(build_line(line, i))

        return ans
```

[Back to Problem Statement](./index.md)
