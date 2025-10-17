class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        m = len(s)
        n = len(t)

        if m == 0:
            return True
        elif n < m:
            return False

        j = 0
        for i in range(n):
            if s[j] == t[i]:
                j += 1

            if j == m:
                return True

        return j == m


if __name__ == "__main__":
    solution = Solution()
    print(solution.isSubsequence(s="abc", t="ahbgdc"))
    print(solution.isSubsequence(s="axc", t="ahbgdc"))
