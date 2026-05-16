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
        # 转化为字符
        s = str(num)
        # 取123、234、345并存储为元素为整数类型的列表
        result = [int(s[i:i+3]) for i in range(len(s) - 2)]
        # 判断是否符合判定条件
        if result[0] % k == 0 and result[1] % k == 0 and result[2] % k == 0:
            print(num)
            flag = True
    if flag == False:
        print("No")


if __name__ == "__main__":
    main()
