from itertools import repeat
import re
from functools import lru_cache
from types import NoneType

def parse_lines(p):
    a, b = p.strip().split()
    a = "?".join(repeat(a, 5))
    b = ",".join(repeat(b, 5))
    return a.strip("."), tuple(map(int, b.split(",")))

with open("day12/input.txt", "r") as fp:
    d = list(map(parse_lines, fp.readlines()))

# print(d)
@lru_cache(maxsize=None)
def ways(pat, nums):
    # first block needs to be made
    if not pat:
        return not nums # no blocks should be left if no places left

    # if there is a block capable of storing the nums block without being mis-sized
    # dont substitute the block and substitute later if not required, (no #)
    w = 0
    if nums and re.match(f"[?#]{{{nums[0]}}}(?:[?.]|$)", pat) is not None:
        w += ways(pat[nums[0] + 1:], nums[1:])

    if pat[0] != '#':
        w += ways(pat[1:], nums)

    return w

print(sum(ways(pat, nums) for pat, nums in d))