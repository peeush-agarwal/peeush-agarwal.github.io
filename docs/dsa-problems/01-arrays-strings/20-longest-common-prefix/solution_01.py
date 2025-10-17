from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        min_len = len(strs[0])
        for st in strs[1:]:
            min_len = min(min_len, len(st))

        ans = ""
        for i in range(min_len):
            ch = strs[0][i]
            ch_diff = False
            for st in strs[1:]:
                if st[i] != ch:
                    ch_diff = True
                    break
            if ch_diff:
                break
            else:
                ans += ch

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(solution.longestCommonPrefix(strs=["flower", "flow", "flight"]))
