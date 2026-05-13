// P1035 [NOIP 2002 普及组] 级数求和
// Author: Dhgaj
// Date: 2026-05-13

#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int solve(int k){
        int n=1;
        double Sn=1.0;

        while (Sn<=k){
            n++;
            Sn+=1.0/n;
        }

        return n;
    }
};

int main() {
    int k;
    cin >>k;

    Solution solution;
    
    cout<<solution.solve(k);

    return 0;
}
