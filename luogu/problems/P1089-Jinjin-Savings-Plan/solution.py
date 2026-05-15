# P1089 [NOIP 2004 提高组] 津津的储蓄计划
# Author: Dhgaj
# Date: 2026-05-15

def main():
    # 每月固定获得 300 元
    moneyGet = 300
    sumInHand = 0
    sumInMum = 0

    for i in range(1, 13):
        # 需要花的钱
        needToSpend = int(input())
        # 在手中的钱
        sumInHand = sumInHand + moneyGet - needToSpend

        # 钱不够
        if sumInHand < 0:
            print(-i)
            return

        # 存整百
        if sumInHand // 100 > 0:
            # 存到妈妈手中的钱
            saveToMum = (sumInHand // 100) * 100

            sumInHand -= saveToMum
            sumInMum += saveToMum

    # 最终金额
    print(int(sumInHand + sumInMum * 1.2))


if __name__ == "__main__":
    main()
