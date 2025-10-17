import bisect
from collections import defaultdict


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        letter_indices_table = defaultdict(list)
        for index, letter in enumerate(t):
            letter_indices_table[letter].append(index)

        curr_match_index = -1
        for letter in s:
            if letter not in letter_indices_table:
                return False  # no match at all, early exit

            # greedy match with binary search
            indices_list = letter_indices_table[letter]
            match_index = bisect.bisect_right(indices_list, curr_match_index)
            if match_index != len(indices_list):
                curr_match_index = indices_list[match_index]
            else:
                return False  # no suitable match found, early exit

        return True


if __name__ == "__main__":
    solution = Solution()
    print(solution.isSubsequence(s="abc", t="ahbgdc"))
    print(solution.isSubsequence(s="axc", t="ahbgdc"))
