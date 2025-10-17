# Intuition

To check if two strings are isomorphic, we need to ensure that each character in the first string maps to a unique character in the second string, and that the mapping is consistent throughout both strings.

# Approach

- Use a dictionary to map characters from `s` to `t`.
- Use a set to track which characters in `t` have already been mapped.
- For each character pair, check if the mapping is consistent and that no two characters from `s` map to the same character in `t`.
- If all checks pass, the strings are isomorphic.

# Complexity

- Time complexity:
$$O(n)$$, where $n$ is the length of the strings (each character is processed once).

- Space complexity:
$$O(n)$$, for the mapping and set.

# Code

```python
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        map_dict = {}
        mapped_set = set()

        for s_c, t_c in zip(s, t):
            map_dict[s_c] = map_dict.get(s_c, t_c)
            if map_dict[s_c] != t_c:
                return False

            mapped_set.add(map_dict[s_c])

        if len(map_dict) != len(mapped_set):
            return False

        return True
```

[Back to Problem Statement](./index.md)
