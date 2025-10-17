class Solution:
    def intToRoman(self, num: int) -> str:
        mapper = {
            1000: "M",
            900: "CM",
            500: "D",
            400: "CD",
            100: "C",
            90: "XC",
            50: "L",
            40: "XL",
            10: "X",
            9: "IX",
            5: "V",
            4: "IV",
            1: "I",
        }

        ans = ""
        for x, s in mapper.items():
            s_times = num // x
            ans += s * s_times
            num = num % x

            if num <= 0:
                break

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(solution.intToRoman(num=3749))  # MMMDCCXLIX
    print(solution.intToRoman(num=1994))  # MCMXCIV
    print(solution.intToRoman(num=58))  # LVIII
