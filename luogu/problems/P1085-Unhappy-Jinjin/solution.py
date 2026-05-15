# P1085 [NOIP 2004 普及组] 不高兴的津津
# Author: Dhgaj
# Date: 2026-05-15

def main():
    # 不高兴的程度值
    valueOfUnhappy = 0
    # 最不高兴的一天,默认为0
    dayOfUnhappy = 0
    for i in range(1, 7+1):
        # 输入一行
        timeInSchool, timeInSchedule = map(int, input().split())
        # 计算当天的上课总时长
        sum = timeInSchool+timeInSchedule
        # 如果超过8小时且大于之前的星期数
        if sum > valueOfUnhappy and sum > 8:
            valueOfUnhappy = sum
            dayOfUnhappy = i
    # 输出
    print(dayOfUnhappy)


if __name__ == "__main__":
    main()
