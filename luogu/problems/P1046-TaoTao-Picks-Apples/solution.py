# P1046 [NOIP 2005 普及组] 陶陶摘苹果
# Author: Dhgaj
# Date: 2026-05-14

def main():
    # 苹果的高度列表
    applesHigh = list(map(int, input().split()))
    # 陶陶的手举起时高度
    taoHandHigh = int(input())
    # 椅子高度
    chairHigh = 30
    # 最高能够够到的高度
    maxHigh = taoHandHigh+chairHigh
    # 全局计算能够够到的数量
    sum = 0
    for i in applesHigh:
        if i <= maxHigh:
            sum += 1
    print(sum)


if __name__ == "__main__":
    main()
