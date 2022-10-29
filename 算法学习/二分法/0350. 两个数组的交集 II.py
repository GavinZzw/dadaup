# -*- coding: utf-8 -*-
# @Time    : 2022/10/11 10:39
# @Author  : zzw
# @File    : 0350. 两个数组的交集 II.py

"""
给你两个整数数组 nums1 和 nums2 ，请你以数组形式返回两数组的交集。
返回结果中每个元素出现的次数，应与元素在两个数组中都出现的次数一致（如果出现次数不一致，则考虑取较小值）。可以不考虑输出结果的顺序
"""
from typing import List


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1.sort()
        nums2.sort()

        n1, n2 = len(nums1), len(nums2)
        l1, l2 = 0, 0
        ret = []

        while l1 < n1 and l2 < n2:
            if nums1[l1] == nums2[l2]:
                ret.append(nums1[l1])
                l1 += 1
                l2 += 1
            elif nums1[l1] < nums2[l2]:
                l1 += 1
            else:
                l2 += 1
        return ret


s = Solution()
print(s.intersect([1, 2, 2, 1], [2, 2]))
