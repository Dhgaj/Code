# P1161 开灯
# Author: Dhgaj
# Date: 2026-05-22


def main():
    n = int(input())

    # 存储当前亮着的灯
    lights = set()

    for _ in range(n):

        # 读取输入
        ai, ti = input().split()

        ai = float(ai)
        ti = int(ti)

        # 模拟操作
        for j in range(1, ti + 1):

            # 灯编号
            num = int(ai * j)

            # 翻转状态
            if num in lights:
                lights.remove(num)
            else:
                lights.add(num)

    # 最终只剩一个
    print(min(lights))


if __name__ == "__main__":
    main()
