# P1152 欢乐的跳
# Author: Dhgaj
# Date: 2026-05-17

import sys


def main():
    # 读取所有输入数据
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    idx = 0
    while idx < len(tokens):
        n = int(tokens[idx])
        idx += 1

        nums = []
        for _ in range(n):
            nums.append(int(tokens[idx]))
            idx += 1

        # 如果只有一个元素，直接满足条件
        if n == 1:
            print("Jolly")
            continue

        # 记录差值是否出现
        diff_exists = [False] * n

        # 计算相邻元素的绝对差值
        for i in range(1, n):
            diff = abs(nums[i] - nums[i-1])
            # 记录在合法范围 [1, n-1] 内的差值
            if 1 <= diff < n:
                diff_exists[diff] = True

        # 检查是否包含了 1 到 n-1 的所有差值
        if all(diff_exists[1:n]):
            print("Jolly")
        else:
            print("Not jolly")


if __name__ == "__main__":
    main()
