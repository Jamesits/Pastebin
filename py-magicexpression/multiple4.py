#!/bin/python
# -*- coding: utf-8 -*-

# 3. 神奇算式
# 	由4个不同的数字，组成的一个乘法算式，它们的乘积仍然由这4个数字组成。
# 	比如：
# 		210 x 6 = 1260  8 x 473 = 3784 27 x 81 = 2187
# 	都符合要求。
# 	如果满足乘法交换律的算式算作同一种情况，那么，包含上边已列出的3种情况，一共有多少种满足要求的算式。

import itertools

# 把一个 list 里的各位数字连接起来
def cont(d):
    r = 0
    for t in d:
         r = r * 10 + t
    return r

count = 0
a = list(itertools.combinations(range(10), 4)) # 十个数字里面取四个的组合

for i in a:
    #print "Test combination: ", i
    possible_result_set = list(itertools.permutations(i, 4))
    possible_result = []
    for d in possible_result_set:
        if d[0] != 0: # 去掉首位为 0 的情况
            possible_result.append(cont(d))
    #print "Possible result: ", possible_result # 这四位数字组成的所有四位数的 list

    for first_set_digit_count in range(1, 4):	#前一个乘数的位数
        first_num_set = list(itertools.combinations(i, first_set_digit_count)) # 前一个乘数的集合
        for first_num_digits in first_num_set:
            second_num_digits = tuple(set(i).difference(set(first_num_digits))) # 后一个乘数的集合
            #print first_num_digits, second_num_digits
            # Now we got two parts
            first_nums_temp = list(itertools.permutations(first_num_digits, len(first_num_digits)))
            second_nums_temp = list(itertools.permutations(second_num_digits, len(second_num_digits)))
            first_nums = []
            second_nums = []
            for d in first_nums_temp:
                first_nums.append(cont(d))
                # 前一个乘数的所有排列可能性
            for d in second_nums_temp:
                second_nums.append(cont(d))
                # 后一个乘数的所有排列可能性

            #print first_nums, second_nums

            # 验证结果
            for a in first_nums:
                for b in second_nums:
                    if a * b in possible_result:
                        print a, " * ", b, " = ", a * b
                        count += 1

print "Count: ", count / 2
