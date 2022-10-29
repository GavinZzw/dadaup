# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 18:00
# @Author  : zzw
# @File    : 1539. 第 k 个缺失的正整数.py
from typing import List


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        """
        输入：arr = [2,3,4,7,11], k = 5
        输出：9
        解释：缺失的正整数包括 [1,5,6,8,9,10,12,13,...] 。第 5 个缺失的正整数为 9 。

        :param arr:
        :param k:
        :return:
        """
        cur = 1
        for index, num in enumerate(arr):
            d = num - index
            if d != cur:
                k -= d - cur
                cur = d
        return k + arr[-1]


s = Solution()
print(s.findKthPositive([2, 3, 4, 7, 11], 1))
