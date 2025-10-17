# Intuition

To convert an integer to a Roman numeral, repeatedly subtract the largest possible Roman value from the number and append its symbol to the result. Special cases like 4, 9, 40, 90, 400, and 900 use subtractive notation (e.g., IV, IX, XL, XC, CD, CM).

# Approach

- Create a mapping of integer values to Roman symbols, ordered from largest to smallest, including subtractive forms.
- Iterate through the mapping, for each value:
    - Determine how many times the value fits into the number.
    - Append the corresponding symbol that many times to the result.
    - Subtract the value multiplied by its count from the number.
- Continue until the number is reduced to zero.

# Complexity

- Time complexity:
$$O(1)$$ (since the number of Roman numeral symbols is fixed and the loop runs a constant number of times)

- Space complexity:
$$O(1)$$ (output string size is bounded by the input constraints)

# Code

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        mapper = {
            1000: "M",
            900: "CM",
            500: "D",
            400: "CD",
            100: "C",
            90: "XC",
            50: "L",
            40: "XL",
            10: "X",
            9: "IX",
            5: "V",
            4: "IV",
            1: "I",
        }

        ans = ""
        for x, s in mapper.items():
            s_times = num // x
            ans += s * s_times
            num = num % x

            if num <= 0:
                break

        return ans
```

[Back to Problem Statement](./index.md)
