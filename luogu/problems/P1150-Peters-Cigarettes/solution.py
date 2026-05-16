# P1150 Peter 的烟
# Author: Dhgaj
# Date: 2026-05-16

def main():
    # 吸烟有害健康，请诊视自己的身体 ！！！
    # 输入Peter有的n根烟和达到数量k能够换取的条件
    n, k = map(int, input().split())
    # 计算总和
    sum = 0
    # 当有>=k时可以换取
    while n >= k:
        # Peter手中剩余的烟
        n = n-k+1
        # 计算已经换取的烟蒂
        sum += k
    # 输出已经换取的烟蒂和手中剩余的烟
    print(sum+n)


if __name__ == "__main__":
    main()
