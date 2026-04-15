// P1002 [NOIP 2002 普及组] 过河卒

// Code Bebin

#include <iostream>
using namespace std;

long long dp[25][25];
bool mark[25][25];

int main()
{
    // 输入
    int n, m, hx, hy;
    cin >> n >> m >> hx >> hy;

    // 马本身的位置以及能够控制的位置规则
    int dx[9] = {0, -2, -1, 1, 2, 2, 1, -1, -2};
    int dy[9] = {0, -1, -2, -2, -1, 1, 2, 2, 1};

    // 标记马控制点
    for (int i = 0; i < 9; i++)
    {
        int x = hx + dx[i];
        int y = hy + dy[i];
        // 对在棋盘区间访问内的进行标记
        if (x >= 0 && y >= 0 && x <= n && y <= m)
        {
            mark[x][y] = true;
        }
    }

    // 起点
    dp[0][0] = mark[0][0] ? 0 : 1;

    // DP
    for (int i = 0; i <= n; i++)
    {
        for (int j = 0; j <= m; j++)
        {
            // 跳过起点
            if (i == 0 && j == 0)
                continue;
            // 如果是马所控制的位置设为0
            if (mark[i][j])
            {
                dp[i][j] = 0;
                continue;
            }
            // 上面
            if (i > 0)
                dp[i][j] += dp[i - 1][j];
            // 下面
            if (j > 0)
                dp[i][j] += dp[i][j - 1];
        }
    }

    // 输出
    cout << dp[n][m] << endl;

    return 0;
}

// Code End