class Solution:
    def reverseWords(self, s: str) -> str:
        ans = []
        w = []
        i = 0
        while i < len(s):
            if s[i] != " ":
                w.append(s[i])
            elif w:
                w = "".join(w)
                ans.append(w)
                w = []

            i += 1

        if w:
            w = "".join(w)
            ans.append(w)
            w = []

        return " ".join(reversed(ans))


if __name__ == "__main__":
    solution = Solution()
    print(solution.reverseWords(s="the sky is blue"))
    print(solution.reverseWords(s="  hello world  "))
    print(solution.reverseWords(s="a good   example"))
