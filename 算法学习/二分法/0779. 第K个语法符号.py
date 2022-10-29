# -*- coding: utf-8 -*-
# @Time    : 2022/10/20 15:24
# @Author  : zzw
# @File    : 0779. 第K个语法符号.py

"""
我们构建了一个包含 n 行( 索引从 1  开始 )的表。首先在第一行我们写上一个 0。接下来的每一行，将前一行中的0替换为01，1替换为10。

例如，对于 n = 3 ，第 1 行是 0 ，第 2 行是 01 ，第3行是 0110 。
给定行数 n 和序数 k，返回第 n 行中第 k 个字符。（ k 从索引 1 开始）

"""


class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n == 1:
            return 0
        # 上层为self.kthGrammar(n - 1, (k + 1) // 2)，生成下层k位置数字，k & 1判断取生成的第几个
        return self.kthGrammar(n - 1, (k + 1) // 2) ^ 1 ^ (k & 1)
