# P1151 子数整数
# Author: Dhgaj
# Date: 2026-05-16

def main():
    # 输入除数
    k = int(input())

    # 在10000到30000的区间
    minNum = 10000
    maxNum = 30000

    # 标记是否找到符合条件的数
    flag = False

    # 历遍10000到30000
    for num in range(minNum, maxNum+1):
        # 使用数学运算替代字符串切片，大幅提升效率
        sub1 = num // 100
        sub2 = (num // 10) % 1000
        sub3 = num % 1000

        # 判断是否符合判定条件
        if sub1 % k == 0 and sub2 % k == 0 and sub3 % k == 0:
            print(num)
            flag = True
    if not flag:
        print("No")


if __name__ == "__main__":
    main()
