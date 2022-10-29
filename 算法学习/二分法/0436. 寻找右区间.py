# -*- coding: utf-8 -*-
# @Time    : 2022/10/13 14:34
# @Author  : zzw
# @File    : 0436. 寻找右区间.py

"""
给你一个区间数组 intervals ，其中 intervals[i] = [starti, endi] ，且每个 starti 都 不同 。

区间 i 的 右侧区间 可以记作区间 j ，并满足 startj >= endi ，且 startj 最小化 。

返回一个由每个区间 i 的 右侧区间 在 intervals 中对应下标组成的数组。如果某个区间 i 不存在对应的 右侧区间 ，则下标 i 处的值设为 -1 。

"""
from bisect import bisect_left
from typing import List


class Solution:
    def findRightInterval(self, intervals: List[List[int]]) -> List[int]:
        for i, interval in enumerate(intervals):
            interval.append(i)

        intervals.sort()
        n = len(intervals)
        ret = [-1] * n

        for _, end, id in intervals:
            i = bisect_left(intervals, [end])
            if i < n:
                ret[id] = intervals[i][2]
        return ret
