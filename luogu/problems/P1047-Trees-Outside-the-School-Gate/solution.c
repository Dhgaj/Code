// P1047 [NOIP 2005 普及组] 校门外的树
// Author: Dhgaj
// Date: 2026-05-14

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    int l, m;
    scanf("%d %d", &l, &m);
    int diff[l + 2];
    // 初始化
    memset(diff, 0, sizeof(diff));
    // 处理每个区间
    for (int i = 0; i < m; i++)
    {
        int u, v;
        scanf("%d %d", &u, &v);
        // 区间开始
        diff[u]++;
        // 区间结束
        diff[v + 1]--;
    }
    // 覆盖计数
    int cur = 0;
    // 剩余树木数量
    int sum = 0;
    // 前缀和恢复
    for (int i = 0; i <= l; i++)
    {
        cur += diff[i];
        // 未被区间覆盖
        if (cur == 0)
        {
            sum++;
        }
    }
    // 输出
    printf("%d", sum);

    return 0;
}
