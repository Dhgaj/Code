// P1003 [NOIP 2011 提高组] 铺地毯
// Author: Dhgaj
// Date: 2026-04-19

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // 输入
    // 地毯数量
    int nums;
    scanf("%d", &nums);
    // 输入坐标存取数组
    int a[nums], b[nums], g[nums], k[nums];
    for (int i = 0; i < nums; i++)
    {
        scanf("%d %d %d %d", &a[i], &b[i], &g[i], &k[i]);
    }
    // 读取的点
    int x, y;
    scanf("%d %d", &x, &y);

    // 倒序查找
    for (int i = nums - 1; i >= 0; i--)
    {
        if ((x >= a[i]) && (x <= a[i] + g[i]) && (y >= b[i]) && (y <= b[i] + k[i]))
        {
            printf("%d\n", i + 1);
            return 0;
        }
    }

    printf("-1\n");

    return 0;
}
