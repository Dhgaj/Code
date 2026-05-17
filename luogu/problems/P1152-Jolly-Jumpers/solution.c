// P1152 欢乐的跳
// Author: Dhgaj
// Date: 2026-05-17

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(void)
{
    int n;

    // 循环读取多组测试数据
    while (scanf("%d", &n) != EOF)
    {
        // 如果只有一个元素，直接满足条件
        if (n == 1)
        {
            int temp;
            scanf("%d", &temp); // 读走唯一元素
            printf("Jolly\n");
            continue;
        }

        // 分配内存：nums 用于存数据，diff_exists 用于记录差值
        int *nums = (int *)malloc(n * sizeof(int));
        bool *diff_exists = (bool *)calloc(n, sizeof(bool));

        // 读取数组元素
        for (int i = 0; i < n; i++)
        {
            scanf("%d", &nums[i]);
        }

        // 计算相邻元素的绝对差值
        for (int i = 1; i < n; i++)
        {
            int diff = abs(nums[i] - nums[i - 1]);
            // 只记录合法范围内的差值
            if (diff >= 1 && diff <= n - 1)
            {
                diff_exists[diff] = true;
            }
        }

        // 判断所有差值是否都出现过
        bool is_jolly = true;
        for (int i = 1; i < n; i++)
        {
            if (!diff_exists[i])
            {
                is_jolly = false;
                break;
            }
        }

        // 输出结果
        if (is_jolly)
        {
            printf("Jolly\n");
        }
        else
        {
            printf("Not jolly\n");
        }

        // 释放内存
        free(nums);
        free(diff_exists);
    }

    return 0;
}
