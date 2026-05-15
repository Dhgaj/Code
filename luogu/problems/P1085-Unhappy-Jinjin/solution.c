// P1085 [NOIP 2004 普及组] 不高兴的津津
// Author: Dhgaj
// Date: 2026-05-15

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // 不高兴的程度值
    int valueOfUnhappy = 0;
    // 最不高兴的一天,默认为0
    int dayOfUnhappy = 0;
    
    for (int i = 1; i <= 8; i++)
    {
        int timeInSchool, timeInSchedule, sum;
        scanf("%d %d", &timeInSchool, &timeInSchedule);
        // 计算当天的上课总时长
        sum = timeInSchool + timeInSchedule;
        // 如果超过8小时且大于之前的星期数
        if (sum > valueOfUnhappy && sum > 8)
        {
            valueOfUnhappy = sum;
            dayOfUnhappy = i;
        }
    }
    printf("%d", dayOfUnhappy);

    return 0;
}
