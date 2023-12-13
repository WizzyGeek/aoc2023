
import numpy as np

with open("day13/proc.txt", "r") as fp:
# with open("day13/example.txt", "r") as fp:
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

def som(arr, offset, idxs, r):
    for i in idxs:
        # print(i, offset)
        if i - offset >= 0 and i + offset + 1 < r:
            if np.array_equal(arr[i - offset], arr[i + offset + 1]):
                yield i
            else:
                continue
        yield i

def get_vert(arr):
    # print("---")
    r = arr.shape[0]
    idxs = iter(range(r - 1))
    for i in range(r // 2):
        idxs = som(arr, i, idxs, r)
    return next(idxs, None)

def get(arr):
    v = get_vert(arr)
    if v is None:
        return 100 * (get_vert(arr) + 1)
    return v + 1

print(sum(map(get, d)))