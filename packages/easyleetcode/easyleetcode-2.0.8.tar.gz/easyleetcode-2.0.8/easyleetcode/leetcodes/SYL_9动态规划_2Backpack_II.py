
def ZeroOnePack(V, weight, value):
    """
    0-1 背包问题(每个物品只能取0次, 或者1次)
    :param V: 背包总容量, 如V=15
    :param weight: 每个物品的容量数组表示, 如weight=[5,4,7,2,6]
    :param value: 每个物品的价值数组表示, 如value=[12,3,10,3,6]
    :return:  返回最大的总价值
    """
    N = len(value)
    # 初始化f[N+1][V+1]为0, f[i][j]表示前i件物品恰放入一个容量为j的背包可以获得的最大价值
    f = [[0 for col in range(V + 1)] for row in range(N + 1)]

    for i in range(1, N + 1):
        for j in range(1, V + 1):
            if j < weight[i - 1]:  # 总容量j小于物品i的容量时，直接不考虑物品i
                f[i][j] = f[i - 1][j]
            else:
                # 注意由于weight、value数组下标从0开始，第i个物品的容量为weight[i-1],价值为value[i-1]
                f[i][j] = max(f[i - 1][j], f[i - 1][j - weight[i - 1]] + value[i - 1])  # 状态方程
    return f[N][V]


if __name__ == '__main__':
    V, weight, value = 10, [2, 3, 5, 7], [1, 5, 2, 4]
    print(ZeroOnePack(V, weight, value))
