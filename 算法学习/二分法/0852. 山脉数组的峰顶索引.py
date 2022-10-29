# -*- coding: utf-8 -*-
# @Time    : 2022/10/21 10:47
# @Author  : zzw
# @File    : 0852. 山脉数组的峰顶索引.py
"""
符合下列属性的数组 arr 称为 山脉数组 ：
arr.length >= 3
存在 i（0 < i < arr.length - 1）使得：
arr[0] < arr[1] < ... arr[i-1] < arr[i]
arr[i] > arr[i+1] > ... > arr[arr.length - 1]
给你由整数组成的山脉数组 arr ，返回任何满足 arr[0] < arr[1] < ... arr[i - 1] < arr[i] > arr[i + 1] > ... > arr[arr.length - 1] 的下标 i 。
"""
from typing import List


class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:

        l, r = 1, len(arr) - 2

        while l <= r:
            mid = (l + r) // 2
            if arr[mid - 1] < arr[mid] > arr[mid + 1]:
                return mid
            elif arr[mid - 1] < arr[mid]:
                l = mid + 1
            else:
                r = mid - 1


s = Solution()
print(s.peakIndexInMountainArray([0, 2, 1, 0]))
