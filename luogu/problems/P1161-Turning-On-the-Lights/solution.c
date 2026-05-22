// P1161 开灯
// Author: Dhgaj
// Date: 2026-05-22

#include <stdio.h>

int main(void)
{
    // 操作组数
    int n;
    scanf("%d", &n);

    // 灯状态
    int light[2000001] = {0};

    // 输入数据
    double a;
    int t;
    // 灯编号
    int num;

    // 处理每组操作
    for (int i = 0; i < n; i++)
    {
        // 读取浮点数和整数
        scanf("%lf %d", &a, &t);

        // 模拟开关灯
        for (int j = 1; j <= t; j++)
        {
            // 计算灯编号
            num = (int)(a * j);

            // 异或翻转
            light[num] ^= 1;
        }
    }

    // 找最终亮着的灯
    for (int i = 0; i <= 2000000; i++)
    {
        if (light[i] == 1)
        {
            printf("%d\n", i);
            break;
        }
    }

    return 0;
}