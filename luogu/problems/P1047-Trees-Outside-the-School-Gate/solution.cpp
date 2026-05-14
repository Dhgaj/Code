// P1047 [NOIP 2005 普及组] 校门外的树
// Author: Dhgaj
// Date: 2026-05-14

#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    int countTrees(vector<int> &diff, int m, int l)
    {
        for (int i = 0; i < m; i++)
        {
            int u, v;
            cin >> u >> v;
            diff[u]++;
            diff[v + 1]--;
        }

        int cur = 0;
        int sum = 0;

        for (int i = 0; i <= l; i++)
        {
            cur += diff[i];
            if (cur == 0)
            {
                sum++;
            }
        }
        return sum;
    }
};

int main()
{
    Solution solution;
    int l, m, sum;
    cin >> l >> m;
    // 差分数组
    vector<int> diff(l + 2, 0);
    sum = solution.countTrees(diff, m, l);
    cout << sum;
    return 0;
}
