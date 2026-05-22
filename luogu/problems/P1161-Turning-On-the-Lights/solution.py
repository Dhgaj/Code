def main():
    n = int(input())
    light = [0] * 2000001

    for _ in range(n):
        ai, ti = map(float, input().split())
        for j in range(1, int(ti) + 1):
            num = int(ai * j)
            if num >= 2000001:
                break
            light[num] += 1

    for i in range(2000001):
        if light[i] % 2 == 1:
            print(i)
            return

if __name__ == "__main__":
    main()
