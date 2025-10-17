class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        m = len(needle)
        n = len(haystack)

        if n < m:
            return -1

        for i in range(n - m + 1):
            for j in range(m):
                if needle[j] != haystack[i + j]:
                    break

                if j == m - 1:
                    return i

        return -1


if __name__ == "__main__":
    solution = Solution()
    print(solution.strStr(haystack="sadbutsad", needle="sad"))
    print(solution.strStr(haystack="leetcode", needle="eet"))
    print(solution.strStr(haystack="leetcode", needle="leeto"))
