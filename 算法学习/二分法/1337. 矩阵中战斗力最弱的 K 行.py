# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 16:25
# @Author  : zzw
# @File    : 1337. 矩阵中战斗力最弱的 K 行.py
"""
给你一个大小为 m * n 的矩阵 mat，矩阵由若干军人和平民组成，分别用 1 和 0 表示。

请你返回矩阵中战斗力最弱的 k 行的索引，按从最弱到最强排序。

如果第 i 行的军人数量少于第 j 行，或者两行军人数量相同但 i 小于 j，那么我们认为第 i 行的战斗力比第 j 行弱。

军人 总是 排在一行中的靠前位置，也就是说 1 总是出现在 0 之前。
"""
from typing import List


class Solution:
    def kWeakestRows(self, mat: List[List[int]], k: int) -> List[int]:
        """
            输入：mat =
                [[1,1,0,0,0],
                 [1,1,1,1,0],
                 [1,0,0,0,0],
                 [1,1,0,0,0],
                 [1,1,1,1,1]],
                k = 3
                输出：[2,0,3]
                解释：
                每行中的军人数目：
                行 0 -> 2
                行 1 -> 4
                行 2 -> 1
                行 3 -> 2
                行 4 -> 5
                从最弱到最强对这些行排序后得到 [2,0,3,1,4]

        """
        res = []
        for i in range(len(mat[0]) + 1):
            for j in range(len(mat)):
                if i - 1 >= 0 and mat[j][i - 1] == 0:
                    continue
                if i == len(mat[0]) or mat[j][i] == 0:
                    res.append(j)
                if len(res) == k:
                    return res


s = Solution()
print(s.kWeakestRows([[1,1,0,0,0],
                 [1,1,1,1,0],
                 [1,0,0,0,0],
                 [1,1,0,0,0],
                 [1,1,1,1,1]], 3))
