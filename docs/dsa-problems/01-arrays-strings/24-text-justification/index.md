# Text Justification

## Problem Statement

Given an array of strings `words` and an integer `maxWidth`, format the text so that each line has exactly `maxWidth` characters and is fully justified (both left and right).

- Pack words greedily: fit as many words as possible in each line.
- Pad extra spaces `' '` so each line has exactly `maxWidth` characters.
- Distribute extra spaces between words as evenly as possible. If spaces cannot be evenly distributed, assign more spaces to the left slots.
- The last line should be left-justified, with no extra spaces between words.

**Notes:**
- A word is a sequence of non-space characters.
- Each word's length is greater than 0 and does not exceed `maxWidth`.
- The input array `words` contains at least one word.

### Examples

**Example 1**

Input:  
`words = ["This", "is", "an", "example", "of", "text", "justification."]`, `maxWidth = 16`

Output:
```
[
    "This    is    an",
    "example  of text",
    "justification.  "
]
```

**Example 2**

Input:  
`words = ["What","must","be","acknowledgment","shall","be"]`, `maxWidth = 16`

Output:
```
[
  "What   must   be",
  "acknowledgment  ",
  "shall be        "
]
```
Explanation: The last line is left-justified. Lines with a single word are also left-justified.

**Example 3**

Input:  
`words = ["Science","is","what","we","understand","well","enough","to","explain","to","a","computer.","Art","is","everything","else","we","do"]`, `maxWidth = 20`

Output:
```
[
  "Science  is  what we",
  "understand      well",
  "enough to explain to",
  "a  computer.  Art is",
  "everything  else  we",
  "do                  "
]
```

### Constraints

- `1 <= words.length <= 300`
- `1 <= words[i].length <= 20`
- `words[i]` consists of only English letters and symbols.
- `1 <= maxWidth <= 100`
- `words[i].length <= maxWidth`

## Code Template

```python
class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        # Your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses a greedy algorithm to pack words into lines and distribute spaces evenly.

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
