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
        // 数学提取连续三个数字（直接通过除法和取余运算，避免高开销的字符串转换）
        int sub1 = num / 100;         // 取前三位 (例 12345 / 100 = 123)
        int sub2 = (num / 10) % 1000; // 取中间三位 (例 12345 / 10 % 1000 = 234)
        int sub3 = num % 1000;        // 取后三位 (例 12345 % 1000 = 345)

        // 判断是否符合条件
        if (sub1 % k == 0 && sub2 % k == 0 && sub3 % k == 0)
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