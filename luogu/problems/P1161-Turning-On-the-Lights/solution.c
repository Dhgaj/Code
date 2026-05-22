#include <stdio.h>

#define MAX 2000001

int main(void)
{
    int n;
    scanf("%d", &n);

    int light[MAX] = {0};

    double a;
    int t;
    for (int i = 0; i < n; i++)
    {
        scanf("%lf %d", &a, &t);
        for (int j = 1; j <= t; j++)
        {
            int num = (int)(a * j);
            if (num >= MAX) break;
            light[num]++;
        }
    }

    for (int i = 0; i < MAX; i++)
    {
        if (light[i] % 2 == 1)
        {
            printf("%d\n", i);
            break;
        }
    }

    return 0;
}
