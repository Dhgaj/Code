# P1035 [NOIP 2002 普及组] 级数求和
# Author: Dhgaj
# Date: 2026-05-13

def main():
    # 输入
    k=int(input())
    Sn=0
    n=1
    while Sn<=k:
        Sn+=(1/n)
        n+=1
    print(n-1)

if __name__ == "__main__":
    main()
