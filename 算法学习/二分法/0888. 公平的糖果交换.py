# -*- coding: utf-8 -*-
# @Time    : 2022/10/18 10:54
# @Author  : zzw
# @File    : 0888. 公平的糖果交换.py

"""
输入两个数组，计算交换两个数组中一个数，使得两个数组和相等，返回交换的两个数
输入：aliceSizes = [1,1], bobSizes = [2,2]
输出：[1,2]
"""
from typing import List


class Solution:
    def fairCandySwap(self, aliceSizes: List[int], bobSizes: List[int]) -> List[int]:
        """
        如果存在x,y交换使得两数组和相等则sum1-x+y=sum2-y+x
        x = (sum1 - sum2) / 2 + y
        :param aliceSizes:
        :param bobSizes:
        :return:
        """
        sum1 = sum(aliceSizes)
        sum2 = sum(bobSizes)

        s = set(bobSizes)
        sub = (sum1 - sum2) / 2
        for x in aliceSizes:
            if x - sub in s:
                return [x, x - sub]


s = Solution()
print(s.fairCandySwap([2], [1, 3]))
