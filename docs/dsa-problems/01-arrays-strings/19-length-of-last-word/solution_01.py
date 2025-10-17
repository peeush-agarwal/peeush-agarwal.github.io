class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        n = len(s)

        ans = 0
        first_char = None
        for i in range(n - 1, -1, -1):
            c = s[i]
            if c == " " and first_char is not None:
                break
            elif c != " ":
                ans += 1
                first_char = first_char or c

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(solution.lengthOfLastWord("Hello World"))  # Output: 5
    print(solution.lengthOfLastWord("   fly me   to   the moon  "))  # Output: 4
    print(solution.lengthOfLastWord("luffy is still joyboy"))  # Output: 6
