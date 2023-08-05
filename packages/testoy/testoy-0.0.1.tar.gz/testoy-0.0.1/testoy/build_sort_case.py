import random

def build_sort_case(l, h, length, n):
    """Returns a test case set that suits your need for sorting
    l: lowest number in the test array (inclusive)
    h: highest number in the test array (inclusive)
    length: length of the test array
    n: the number of test case set you need
    """
    arr_tcs = []
    for _ in range(n):
        tc_set = [random.randint(l, h) for _ in range(length)]
        arr_tcs.append((tc_set, sorted(tc_set)))
    return arr_tcs

print(build_sort_case(-10, 15, 10, 8))