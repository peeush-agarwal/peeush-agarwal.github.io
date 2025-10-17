class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        map_dict = {}
        mapped_set = set()

        for s_c, t_c in zip(s, t):
            map_dict[s_c] = map_dict.get(s_c, t_c)
            if map_dict[s_c] != t_c:
                return False

            mapped_set.add(map_dict[s_c])

        if len(map_dict) != len(mapped_set):
            return False

        return True


if __name__ == "__main__":
    solution = Solution()
    print(solution.isIsomorphic(s="egg", t="add"))
    print(solution.isIsomorphic(s="foo", t="bar"))
    print(solution.isIsomorphic(s="paper", t="title"))
    print(solution.isIsomorphic(s="badc", t="baba"))
