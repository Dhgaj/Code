// P1150 Peter 的烟
// Author: Dhgaj
// Date: 2026-05-16

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // 吸烟有害健康，请诊视自己的身体 ！！！
    //  输入Peter有的n根烟和达到数量k能够换取的条件
    int n, k, sum;
    scanf("%d %d", &n, &k);
    sum = 0;
    // 当有>=k时可以换取
    while (n >= k)
    {
        // Peter手中剩余的烟
        n = n - k + 1;
        // 计算已经换取的烟蒂
        sum += k;
    }

    printf("%d", sum + n);

    return 0;
}
