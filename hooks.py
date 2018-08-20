COL_SUMS = [28, 552, 64, 15, 86, 1304, 170, 81, 810]
ROW_SUMS = [810, 585, 415, 92, 67, 136, 8, 225, 567]
N = 9

# 4 corners
# 2n-1 choose n placements for n-hook
# each hook's row and col must be completed after placing numbers
# after placing a hook, recurse with n-1 on smaller board -> backtrack if nothing works

import itertools

def solve(grid, curr_num, top, bot, left, right):
    TR, TL, BL, BR = 0, 1, 2, 3
    # print "Curr num:", curr_num

    if curr_num == 0:
        return True

    # indices for the hooks
    top_ind = [(top*N+left) + x for x in range(curr_num)]
    bot_ind = [(bot*N+left) + x for x in range(curr_num)]
    left_ind = [(top*N+left) + x*N for x in range(curr_num)]
    right_ind = [(top*N+right) + x*N for x in range(curr_num)]

    r = range(4)
    if curr_num == 9:
        r = [0]
    if curr_num == 8:
        r = [0]

    for hook in r:
        # print "Curr num:", curr_num, "-- Hook num:", hook
        if hook == TR:
            indices = list(set(top_ind + right_ind))
        elif hook == TL:
            indices = list(set(top_ind + left_ind))
        elif hook == BL:
            indices = list(set(bot_ind + left_ind))
        elif hook == BR:
            indices = list(set(bot_ind + right_ind))
        else:
            print "err: bad hook num"

        for chosen_indices in itertools.combinations(indices, curr_num):
            for i in chosen_indices:
                grid[i] = curr_num

            top_row = grid[top*N:top*N+N]
            bot_row = grid[bot*N:bot*N+N]
            left_col = [grid[left+x*N] for x in range(N)]
            right_col = [grid[right+x*N] for x in range(N)]

            if hook == TR and product_sum(top_row) == ROW_SUMS[top] and product_sum(right_col) == COL_SUMS[right]:
                if solve(grid, curr_num-1, top+1, bot, left, right-1):
                    return True
            elif hook == TL and product_sum(top_row) == ROW_SUMS[top] and product_sum(left_col) == COL_SUMS[left]:
                if solve(grid, curr_num-1, top+1, bot, left+1, right):
                    return True
            elif hook == BL and product_sum(bot_row) == ROW_SUMS[bot] and product_sum(left_col) == COL_SUMS[left]:
                if solve(grid, curr_num-1, top, bot-1, left+1, right):
                    return True
            elif hook == BR and product_sum(bot_row) == ROW_SUMS[bot] and product_sum(right_col) == COL_SUMS[right]:
                if solve(grid, curr_num-1, top, bot-1, left, right-1):
                    return True

            # reset hook after conflict
            for i in indices:
                grid[i] = 0

    return False

def product_sum(row):
    # split list along 0's
    mainlist = []
    sublist = []
    for el in row:
        if el == 0:
            if len(sublist) > 0:
                mainlist.append(sublist)
            sublist = []
        else:
            sublist.append(el)
    if len(sublist) > 0:
        mainlist.append(sublist)
    # calc
    products = map(lambda nums: reduce(lambda x,y: x*y, nums), mainlist)
    sums = reduce(lambda x,y: x+y, products)
    return sums

print "Solving.."
import time
start = time.time()
grid = [0 for _ in range(N*N)]
curr_num = N
top, bot, left, right = 0, N-1, 0, N-1
solve(grid, curr_num, top, bot, left, right)
print "Time taken:", time.time() - start

solution = [grid[i*N:i*N+N] for i in range(N)]
"""
solution = [
[9, 9, 0, 0, 0, 0, 9, 9, 9],
[0, 8, 8, 0, 8, 8, 8, 0, 9],
[0, 0, 7, 7, 7, 0, 0, 8, 9],
[6, 6, 0, 0, 0, 0, 7, 8, 0],
[0, 5, 5, 0, 0, 6, 7, 0, 0],
[4, 4, 0, 4, 5, 6, 0, 0, 0],
[0, 2, 0, 0, 0, 6, 0, 0, 0],
[3, 2, 1, 0, 5, 6, 7, 0, 9],
[3, 0, 3, 4, 5, 0, 7, 8, 9]
]
"""

print "Solution Grid---"
for line in solution:
    print line

solution = map(lambda row: map(lambda el: 1 if el == 0 else 0, row), solution)

from scipy.ndimage import measurements
labels, num = measurements.label(solution)
areas = measurements.sum(solution, labels, index=range(1, num+1))
print "Areas:", areas
print "Solution:", reduce(lambda x,y: x*y, areas)

"""
[0, 0, 1, 1, 1, 1, 0, 0, 0]
[1, 0, 0, 1, 0, 0, 0, 1, 0]
[1, 1, 0, 0, 0, 1, 1, 0, 0]
[0, 0, 1, 1, 1, 1, 0, 0, 1]
[1, 0, 0, 1, 1, 0, 0, 1, 1]
[0, 0, 1, 0, 0, 0, 1, 1, 1]
[1, 0, 1, 1, 1, 0, 1, 1, 1]
[0, 0, 0, 1, 0, 0, 0, 1, 0]
[0, 1, 0, 0, 0, 1, 0, 0, 0]
"""
# Areas: [  5.   3.   1.   8.  10.   1.   5.   1.   1.   1.]
# Solution: 6000.0
