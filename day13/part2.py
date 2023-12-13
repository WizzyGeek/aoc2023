
import numpy as np

# with open("day13/proc.txt", "r") as fp:
with open("day13/proc.txt", "r") as fp:
    d = map(
        lambda k: np.array(list(
            map(
                lambda p: list(
                    map(
                        lambda c: c == "1",
                        p
                    )
                ),
                k.strip().removesuffix(",").split(",")
            )
        )),
        fp.readlines()
    )

def sum_itr(sum):
    for i in range(sum // 2 + 1):
        yield i, sum - i

def pair_itr_itr(arr):
    r = arr.shape[0]
    for i in range(r - 1):
        yield i, filter(lambda k: k[1] < r and k[0] >= 0 and k[0] < k[1], sum_itr(2 * i + 1))

def get_vert(arr):
    for pos, i in pair_itr_itr(arr):
        can_fix = True
        valid = True
        for r0, r1 in i:
            ch: np.ndarray = arr[r0] == arr[r1]
            # print(r0, r1, pos, arr[r0], arr[r1])
            if (ch).all():
                continue
            elif ch.sum() == ch.shape[0] - 1 and can_fix:
                can_fix = False
            else:
                valid = False
                break
        print(valid, can_fix)
        if valid and not can_fix:
            print("_")
            return pos
    return None

# def som(arr, offset, idxs, r):
#     for i in idxs:
#         # print(i, offset)
#         if i - offset >= 0 and i + offset + 1 < r:
#             if np.array_equal(arr[i - offset], arr[i + offset + 1]):
#                 yield i
#             else:
#                 continue
#         yield i

# def get_vert(arr):
#     # print("---")
#     r = arr.shape[0]
#     idxs = iter(range(r - 1))
#     for i in range(r // 2):
#         idxs = som(arr, i, idxs, r)
#     return next(idxs, None)

# def get(arr):
#     v = get_vert(arr.T)
#     if v is None:
#         v = get_vert(arr)
#         if v is not None:
#             return 100 * (v + 1)
#     return v + 1

# print(sum(map(get, d)))

def get(arr):
    v = get_vert(arr.T)
    if v is None:
        return 100 * (get_vert(arr) + 1)
    return v + 1

print(sum(map(get, d)))