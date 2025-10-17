from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict

        ans = defaultdict(list)

        for s in strs:
            cnt = [0] * 26
            for c in s:
                cnt[ord(c) - ord("a")] += 1

            ans[tuple(cnt)].append(s)

        return list(ans.values())


if __name__ == "__main__":
    solution = Solution()
    print(solution.groupAnagrams(strs=["eat", "tea", "tan", "ate", "nat", "bat"]))
