// P1046 [NOIP 2005 普及组] 陶陶摘苹果
// Author: Dhgaj
// Date: 2026-05-14

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // 苹果的数量
    int num = 10;
    // 苹果高度的数组
    int applesHigh[num];
    // 涛涛的手伸直后能够到的高度
    int taoHigh;
    // 椅子的高度
    int chairHigh = 30;
    // 总高度
    int totalHigh;
    // 够到的总数
    int sum = 0;
    // 输入
    for (int i = 0; i < num; i++)
    {
        scanf("%d", &applesHigh[i]);
    }
    scanf("%d", &taoHigh);

    totalHigh = taoHigh + chairHigh;

    for (int i = 0; i < num; i++)
    {
        // 当苹果高度小于最高够到的高度时
        if (applesHigh[i] <= totalHigh)
        {
            sum++;
        }
    }
    // 输出结果
    printf("%d", sum);

    return 0;
}
