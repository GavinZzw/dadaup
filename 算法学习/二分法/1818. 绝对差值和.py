# -*- coding: utf-8 -*-
# @Time    : 2022/10/19 11:41
# @Author  : zzw
# @File    : 1818. 绝对差值和.py

"""
给你两个正整数数组 nums1 和 nums2 ，数组的长度都是 n 。

数组 nums1 和 nums2 的 绝对差值和 定义为所有 |nums1[i] - nums2[i]|（0 <= i < n）的 总和（下标从 0 开始）。

你可以选用 nums1 中的 任意一个 元素来替换 nums1 中的 至多 一个元素，以 最小化 绝对差值和。

在替换数组 nums1 中最多一个元素 之后 ，返回最小绝对差值和。因为答案可能很大，所以需要对 1^9 + 7 取余 后返回。
"""

from typing import List
import bisect


class Solution:
    def minAbsoluteSumDiff(self, nums1: List[int], nums2: List[int]) -> int:
        """

        :param nums1:
        :param nums2:
        :return:
        """
        const_mod = 1000000007
        n = len(nums1)
        arr = sorted(nums1)
        sum, maxDiff = 0, 0
        for i in range(n):
            # 计算绝对值差值
            preDiff = abs(nums1[i] - nums2[i])
            # 二分法计算nums1中和当前nums2[i]差值最小的
            j = bisect.bisect_left(arr, nums2[i])
            # 如果存在当前nums2[i]差值最小的arr[j]，算出该差值和没交换的差值最大值并保存,这样使得交换后总和减少最多
            if j < n:
                maxDiff = max(maxDiff, preDiff - (arr[j] - nums2[i]))
            if j > 0:
                maxDiff = max(maxDiff, preDiff - (nums2[i] - arr[j - 1]))
            sum += preDiff
        return (sum - maxDiff) % const_mod


s = Solution()
print(s.minAbsoluteSumDiff([1, 10, 4, 4, 2, 7], [9, 3, 5, 1, 7, 4]))
