# P1003 [NOIP 2011 提高组] 铺地毯
# Author: Dhgaj
# Date: 2026-04-19

def main():
    # 输入
    nums = int(input())
    matrix = []
    for i in range(nums):
        matrix.append(list(map(int, input().split())))
    x, y = map(int, input().split())

    # 倒序查找
    for i in range(nums - 1, -1, -1):
        # 解包
        a, b, g, k = matrix[i]

        # 判断是否覆盖
        if a <= x <= a + g and b <= y <= b + k:
            print(i + 1)
            break
    else:
        print(-1)


if __name__ == "__main__":
    main()
