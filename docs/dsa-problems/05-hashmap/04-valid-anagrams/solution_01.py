from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        t_count = Counter(t)
        for c in s:
            if c in t_count:
                t_count[c] -= 1

        for k, v in t_count.items():
            if v != 0:
                return False

        return True


if __name__ == "__main__":
    solution = Solution()
    print(solution.isAnagram(s="anagram", t="nagaram"))
    print(solution.isAnagram(s="rat", t="car"))
