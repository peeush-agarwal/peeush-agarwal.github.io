class Solution:
    def isHappy(self, n: int) -> bool:
        def get_next(x):
            s = 0
            while x > 0:
                d = x % 10
                s += d**2
                x = x // 10

            return s

        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = get_next(n)

        return n == 1


if __name__ == "__main__":
    solution = Solution()
    print(solution.isHappy(n=19))
    print(solution.isHappy(n=2))
