# Integer to Roman

## Problem Description

Given an integer `num` where $1 \leq \text{num} \leq 3999$, convert it to its Roman numeral representation.

### Roman Numeral Symbols

| Symbol | Value |
|--------|-------|
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

### Conversion Rules

- Process each decimal place from highest to lowest.
- For values starting with 4 or 9, use subtractive notation:
    - 4: IV, 9: IX
    - 40: XL, 90: XC
    - 400: CD, 900: CM
- Otherwise, append the largest symbol not exceeding the remaining value, subtract it, and continue.
- Only I, X, C, and M can repeat consecutively (up to 3 times). V, L, and D cannot repeat; use subtractive forms instead of four repeats.

### Return

Return the Roman numeral string corresponding to `num`.

### Examples

**Example 1**

```
Input: num = 3749
Output: "MMMDCCXLIX"
Explanation:
- 3000 → MMM
- 700 → DCC
- 40 → XL
- 9 → IX
```

**Example 2**

```
Input: num = 58
Output: "LVIII"
Explanation:
- 50 → L
- 8 → VIII
```

**Example 3**

```
Input: num = 1994
Output: "MCMXCIV"
Explanation:
- 1000 → M
- 900 → CM
- 90 → XC
- 4 → IV
```

### Constraints

- $1 \leq \text{num} \leq 3999$

## Code Template

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        # Write your code here
        pass
```

## Solutions

- [Solution 1](./solution_01.md): This approach uses a mapping of integer values to Roman symbols and iteratively constructs the Roman numeral by subtracting values and appending symbols. The time and space complexity are both O(1) due to the fixed number of Roman numeral symbols.

[Back to Problem List](../index.md) | [Back to Categories](../../index.md)
