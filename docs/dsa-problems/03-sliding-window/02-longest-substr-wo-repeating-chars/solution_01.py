class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        chars_index = [-1] * 128
        left, right = 0, 0
        res = -float("inf")

        for right in range(len(s)):
            ch_ascii = ord(s[right])

            ch_index = chars_index[ch_ascii]

            while ch_index != -1 and (left <= ch_index <= right):
                left = ch_index + 1

            chars_index[ch_ascii] = right
            res = max(res, right - left + 1)

        return int(res if res >= 0 else 0)


if __name__ == "__main__":
    solution = Solution()
    print(solution.lengthOfLongestSubstring(s="abcabcbb"))
    print(solution.lengthOfLongestSubstring(s="bbbbb"))
    print(solution.lengthOfLongestSubstring(s="pwwkew"))
