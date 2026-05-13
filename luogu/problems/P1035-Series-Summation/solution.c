// P1035 [NOIP 2002 普及组] 级数求和
// Author: Dhgaj
// Date: 2026-05-13

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int k;
    int n=1;
    double Sn=1.0;
    scanf("%d",&k);
    
    while(Sn<=k)
    {
        n++;
        Sn+=(1.0/n);
    }
    printf("%d",n);

    return 0;
    
}
