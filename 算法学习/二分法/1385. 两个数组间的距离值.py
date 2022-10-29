# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 16:29
# @Author  : zzw
# @File    : 1385. 两个数组间的距离值.py

"""
给你两个整数数组 arr1 ， arr2 和一个整数 d ，请你返回两个数组之间的 距离值 。

「距离值」 定义为符合此距离要求的元素数目：对于元素 arr1[i] ，不存在任何元素 arr2[j] 满足 |arr1[i]-arr2[j]| <= d 。
"""
from typing import List


class Solution:
    def findTheDistanceValue(self, arr1: List[int], arr2: List[int], d: int) -> int:
        """
        输入：arr1 = [4,5,8], arr2 = [10,9,1,8], d = 2
        输出：2
        解释：
        对于 arr1[0]=4 我们有：
        |4-10|=6 > d=2
        |4-9|=5 > d=2
        |4-1|=3 > d=2
        |4-8|=4 > d=2
        所以 arr1[0]=4 符合距离要求

        对于 arr1[1]=5 我们有：
        |5-10|=5 > d=2
        |5-9|=4 > d=2
        |5-1|=4 > d=2
        |5-8|=3 > d=2
        所以 arr1[1]=5 也符合距离要求

        对于 arr1[2]=8 我们有：
        |8-10|=2 <= d=2
        |8-9|=1 <= d=2
        |8-1|=7 > d=2
        |8-8|=0 <= d=2
        存在距离小于等于 2 的情况，不符合距离要求

        故而只有 arr1[0]=4 和 arr1[1]=5 两个符合距离要求，距离值为 2

        :param arr1:
        :param arr2:
        :param d:
        :return:
        """
        arr2.sort()
        arr1_len = len(arr1)
        arr2_len = len(arr2)
        res = arr1_len
        for i in range(arr1_len):
            l, r = 0, arr2_len - 1
            while l <= r:
                mid = (l + r) // 2
                print(mid, i)
                if abs(arr2[mid] - arr1[i]) <= d:
                    res -= 1
                    break
                elif arr2[mid] > arr1[i]:
                    r = mid - 1
                else:
                    l = mid + 1
        return res


s = Solution()
print(s.findTheDistanceValue([2, 1, 100, 3], [-5, -2, 10, -3, 7], 3))
