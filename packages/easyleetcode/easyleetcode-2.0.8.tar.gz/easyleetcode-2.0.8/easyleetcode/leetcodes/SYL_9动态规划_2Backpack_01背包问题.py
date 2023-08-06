class Solution:
    def backPack(self, M, A):
        if A == None or len(A) == 0:
            return 0
        N = len(A)
        # bp = [N + 1][M + 1]
        bp = [[0] * (M + 1) for _ in range(N + 1)]

        for i in range(N):
            for j in range(M + 1):
                # i号size已经大于j，则不能装，那么，第
                if A[i] > j:
                    bp[i + 1][j] = bp[i][j]
                else:
                    # 不加入，或者加入物品。
                    # 不加时，取钱i个物品，重量不超过j的最大重量，等价于取前i-1个物品，重量不超过j时的重量。（bp[i][j]）
                    # 加入时，取钱i个物品，重量不超过j的最大重量，等价于取前i-1个物品，重量不超过j-A[i]时的重量 + z装下这个i号物品的重量A[i]。（bp[i][j - A[i]] + A[i]）
                    bp[i + 1][j] = max(bp[i][j], bp[i][j - A[i]] + A[i])
        # 数组前N-1个物品（全部物品）中，选出重量不超过M时总重量的最大值。（最优答案）
        return bp[N - 1 + 1][M]


if __name__ == '__main__':
    # 0/1背包问题
    print(Solution().backPack(11, [2, 3, 5, 7]))
    print(Solution().backPack(12, [2, 3, 5, 7]))
