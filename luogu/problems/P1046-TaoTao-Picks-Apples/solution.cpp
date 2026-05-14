// P1046 [NOIP 2005 普及组] 陶陶摘苹果
// Author: Dhgaj
// Date: 2026-05-14

#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    // 计算能够摘到多少苹果
    int countApples(vector<int> &applesHigh, int taoHigh)
    {
        // 椅子高度
        int chairHigh = 30;

        // 总高度
        int totalHigh = taoHigh + chairHigh;

        // 能摘到的数量
        int sum = 0;

        // 遍历所有苹果
        for (int i = 0; i < applesHigh.size(); i++)
        {
            // 判断是否能够到
            if (applesHigh[i] <= totalHigh)
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
    int num = 10;
    // 苹果高度数组
    vector<int> applesHigh(num);

    // 输入苹果高度
    for (int i = 0; i < num; i++)
    {
        cin >> applesHigh[i];
    }

    // 涛涛能够到的高度
    int taoHigh;
    cin >> taoHigh;

    // 调用方法
    int sum = solution.countApples(applesHigh, taoHigh);

    // 输出
    cout << sum << endl;

    return 0;
}