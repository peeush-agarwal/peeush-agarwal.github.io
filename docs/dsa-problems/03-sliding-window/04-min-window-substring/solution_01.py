from collections import Counter, defaultdict


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        m = len(s)

        dict_t = Counter(t)
        required = len(dict_t)

        left, right = 0, 0
        formed = 0
        window_counts = defaultdict(int)
        ans = (float("inf"), left, right)

        for right in range(m):
            character = s[right]
            window_counts[character] += 1

            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1

            while left <= right and formed == required:
                character = s[left]

                if right - left + 1 < ans[0]:
                    ans = (right - left + 1, left, right)

                window_counts[character] -= 1
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1

                left += 1

        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]


if __name__ == "__main__":
    solution = Solution()
    print(solution.minWindow(s="ADOBECODEBANC", t="ABC"))
    print(solution.minWindow(s="a", t="a"))
    print(solution.minWindow(s="a", t="aa"))
