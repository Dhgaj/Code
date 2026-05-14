# P1047 [NOIP 2005 普及组] 校门外的树
# Author: Dhgaj
# Date: 2026-05-14

def main():
    # 马路长度和区间数量
    L, m = map(int, input().split())

    # 差分数组
    diff = [0] * (L + 2)

    # 处理每个区间
    for _ in range(m):
        u, v = map(int, input().split())

        # 区间开始 +1
        diff[u] += 1
        # 区间结束后一个位置 -1
        diff[v + 1] -= 1

    # 当前是否有区域覆盖的计数值
    cur = 0

    # 剩余树木数量
    sum = 0

    # 前缀和恢复
    for i in range(L + 1):
        cur += diff[i]

        # 没被覆盖
        if cur == 0:
            sum += 1
    # 输出
    print(sum)


if __name__ == "__main__":
    main()
