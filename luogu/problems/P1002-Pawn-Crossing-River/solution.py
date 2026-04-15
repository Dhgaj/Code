# P1002 [NOIP 2002 普及组] 过河卒

# Code Begin

# 将输入转化为数组
nums = list(map(int, input().split()))

# 目的地坐标
B = (nums[0], nums[1])
# 马的坐标
Horse = (nums[2], nums[3])
# 马能够控制的范围以及自身
horse_control_rules = [(-2, -1), (-1, -2), (1, -2),
                       (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (0, 0)]
horse_control = [[i[0]+Horse[0], i[1]+Horse[1]] for i in horse_control_rules]

# 初始化 DP (棋盘)
dp = [[0]*(B[1]+1) for _ in range(B[0]+1)]

# 起点
if [0, 0] not in horse_control:
    dp[0][0] = 1

# 填表
for i in range(B[0]+1):
    for j in range(B[1]+1):

        # 跳过起点
        if i == 0 and j == 0:
            continue

        # 被马控制
        if [i, j] in horse_control:
            dp[i][j] = 0
            continue

        # 上面
        if i > 0:
            dp[i][j] += dp[i-1][j]

        # 左边
        if j > 0:
            dp[i][j] += dp[i][j-1]

# 结果
print(dp[B[0]][B[1]])

# Code End