# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 11:04
# @Author  : zzw
# @File    : 0349. 两个数组的交集.py

"""
给定两个数组 nums1 和 nums2 ，返回 它们的交集 。输出结果中的每个元素一定是唯一的。我们可以不考虑输出结果的顺序 。
"""
from typing import List


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        排序+双指针
        :param nums1:
        :param nums2:
        :return:
        """
        nums1.sort()
        nums2.sort()

        ret = []
        n1 = len(nums1)
        n2 = len(nums2)

        l1, l2 = 0, 0
        while l1 < n1 and l2 < n2:
            if nums1[l1] == nums2[l2]:
                if not ret or nums1[l1] != ret[-1]:
                    ret.append(nums1[l1])
                l1 += 1
                l2 += 1
            elif nums1[l1] < nums2[l2]:
                l1 += 1
            else:
                l2 += 1
        return ret


s = Solution()
print(s.intersection([9, 4, 9, 8, 4], [4, 5, 9]))
