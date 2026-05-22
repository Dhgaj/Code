// P1161 开灯
// Author: Dhgaj
// Date: 2026-05-22

#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    // 核心逻辑
    int solve()
    {
        // 操作组数
        int n;

        cin >> n;

        // 灯状态
        vector<bool> light(2000001, false);

        // 输入数据
        double a;
        int t;

        // 处理每组操作
        for (int i = 0; i < n; i++)
        {
            // 读取输入
            cin >> a >> t;

            // 模拟翻转
            for (int j = 1; j <= t; j++)
            {
                // 灯编号
                int num = (int)(a * j);

                // 异或翻转
                light[num] = !light[num];
            }
        }

        // 找最终亮着的灯
        for (int i = 0; i <= 2000000; i++)
        {
            if (light[i])
            {
                return i;
            }
        }

        return 0;
    }
};

int main()
{
    // 实例化对象
    Solution solution;

    // 调用核心逻辑
    int answer = solution.solve();
    cout << answer;

    return 0;
}