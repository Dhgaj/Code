// P1089 [NOIP 2004 提高组] 津津的储蓄计划
// Author: Dhgaj
// Date: 2026-05-15

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int moneyGet, sumInHand, sumInMum, saveToMum, needToSpend;
    // 每月固定获得 300 元
    moneyGet = 300;
    // 手里的钱
    sumInHand = 0;
    // 存在妈妈那里的钱
    sumInMum = 0;

    // 12 个月
    for (int i = 1; i <= 12; i++)
    {
        // 输入本月花费
        scanf("%d", &needToSpend);

        // 更新当前手里的钱
        sumInHand = sumInHand + moneyGet - needToSpend;

        // 钱不够
        if (sumInHand < 0)
        {
            printf("%d", -i);
            return 0;
        }

        // 存整百
        if ((sumInHand / 100) > 0)
        {
            saveToMum = (sumInHand / 100) * 100;

            sumInHand -= saveToMum;
            sumInMum += saveToMum;
        }
    }

    // 输出最终金额
    printf("%d", sumInHand + (int)(sumInMum * 1.2));

    return 0;
}