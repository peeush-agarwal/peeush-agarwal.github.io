from typing import List


class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        def get_words(i):
            line = []
            line_len = 0

            while i < len(words) and line_len + len(words[i]) <= maxWidth:
                line.append(words[i])
                line_len += len(words[i]) + 1
                i += 1

            return line

        def build_line(line, i):
            total_len = -1
            for w in line:
                total_len += len(w) + 1

            extra_spaces = maxWidth - total_len

            if len(line) == 1 or i == len(words):
                return " ".join(line) + " " * extra_spaces

            word_count = len(line) - 1
            spaces_per_word = extra_spaces // word_count
            needs_extra_space = extra_spaces % word_count

            for j in range(needs_extra_space):
                line[j] += " "

            for j in range(word_count):
                line[j] += " " * spaces_per_word

            return " ".join(line)

        ans = []
        i = 0

        while i < len(words):
            line = get_words(i)
            i += len(line)
            ans.append(build_line(line, i))

        return ans


if __name__ == "__main__":
    solution = Solution()
    print(
        solution.fullJustify(
            words=["This", "is", "an", "example", "of", "text", "justification."],
            maxWidth=16,
        )
    )
    print(
        solution.fullJustify(
            words=["What", "must", "be", "acknowledgment", "shall", "be"],
            maxWidth=16,
        )
    )
    print(
        solution.fullJustify(
            words=[
                "Science",
                "is",
                "what",
                "we",
                "understand",
                "well",
                "enough",
                "to",
                "explain",
                "to",
                "a",
                "computer.",
                "Art",
                "is",
                "everything",
                "else",
                "we",
                "do",
            ],
            maxWidth=20,
        )
    )
