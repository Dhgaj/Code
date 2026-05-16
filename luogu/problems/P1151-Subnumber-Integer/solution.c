// P1151 子数整数
// Author: Dhgaj
// Date: 2026-05-16

#include <stdio.h>

int main()
{
    // 输入除数
    int k;
    scanf("%d", &k);

    // 在10000到30000的区间
    int minNum = 10000;
    int maxNum = 30000;

    // 标记是否找到符合条件的数
    int flag = 0;

    // 遍历10000到30000
    for (int num = minNum; num <= maxNum; num++)
    {
        // 转化为字符串
        char s[10];
        sprintf(s, "%d", num);

        // 存储连续三个数字
        int result[3];

        // 取123
        result[0] =
            (s[0] - '0') * 100 +
            (s[1] - '0') * 10 +
            (s[2] - '0');

        // 取234
        result[1] =
            (s[1] - '0') * 100 +
            (s[2] - '0') * 10 +
            (s[3] - '0');

        // 取345
        result[2] =
            (s[2] - '0') * 100 +
            (s[3] - '0') * 10 +
            (s[4] - '0');

        // 判断是否符合条件
        if (result[0] % k == 0 &&
            result[1] % k == 0 &&
            result[2] % k == 0)
        {
            printf("%d\n", num);

            flag = 1;
        }
    }

    // 如果没有找到
    if (flag == 0)
    {
        printf("No\n");
    }

    return 0;
}