// P1089 [NOIP 2004 提高组] 津津的储蓄计划
// Author: Dhgaj
// Date: 2026-05-15

#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    int SavingPlan(int moneyGet, int sumInHand, int sumInMum)
    {
        int needToSpend, saveToMum;
        for (int i = 1; i <= 12; i++)
        {
            // 输入本月花费
            cin >> needToSpend;

            // 更新当前手里的钱
            sumInHand = sumInHand + moneyGet - needToSpend;

            // 钱不够
            if (sumInHand < 0)
            {
                return -i;
            }

            // 存整百
            if ((sumInHand / 100) > 0)
            {
                saveToMum = (sumInHand / 100) * 100;

                sumInHand -= saveToMum;
                sumInMum += saveToMum;
            }
        }
        return sumInHand+sumInMum*6/5;
    }
};

int main()
{
    int moneyGet, sumInHand, sumInMum, saveToMum;
    // 每月固定获得 300 元
    moneyGet = 300;
    // 手里的钱
    sumInHand = 0;
    // 存在妈妈那里的钱
    sumInMum = 0;

    Solution solution;
    int result=solution.SavingPlan(moneyGet,sumInHand,sumInMum);
    cout << result;

    return 0;
}
