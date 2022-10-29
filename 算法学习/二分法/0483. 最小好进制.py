# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 16:04
# @Author  : zzw
# @File    : 0483. 最小好进制.py

"""
以字符串的形式给出 n , 以字符串的形式返回 n 的最小 好进制  。

如果 n 的  k(k>=2) 进制数的所有数位全为1，则称 k(k>=2) 是 n 的一个 好进制 。

输入：n = "13"
输出："3"
解释：13 的 3 进制是 111。
"""


class Solution:
    def smallestGoodBase(self, n: str) -> str:
        num = int(n)

        def check(x, m):
            """
            计算x进制的m位1
            :param x:
            :param m:
            :return:
            """
            ans = 0
            for _ in range(m):

                # 防止溢出
                if ans > (num - 1) / x:
                    return num + 1
                ans = ans * x + 1
            return ans

        ans = str(num - 1)
        for i in range(64, 0, -1):
            l = 2
            r = num
            while l < r:
                mid = l + (r - l) // 2
                tmp = check(mid, i)
                if tmp == num:
                    return str(mid)
                elif tmp < num:
                    l = mid + 1
                else:
                    r = mid

        return str(ans)

s = Solution()
print(s.smallestGoodBase("13"))