// P1152 欢乐的跳
// Author: Dhgaj
// Date: 2026-05-17

#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

class Solution
{
public:
    bool isJolly(int n, const vector<int> &nums)
    {
        // 只有一个元素时直接符合要求
        if (n == 1)
            return true;

        // 记录 [1, n-1] 差值是否出现过
        vector<bool> diff_exists(n, false);

        // 遍历并计算相邻元素的差值
        for (int i = 1; i < n; ++i)
        {
            int diff = abs(nums[i] - nums[i - 1]);
            // 只记录 [1, n-1] 范围内的差值
            if (diff >= 1 && diff <= n - 1)
            {
                diff_exists[diff] = true;
            }
        }

        // 检查所有差值是否都出现过
        for (int i = 1; i < n; ++i)
        {
            if (!diff_exists[i])
            {
                return false;
            }
        }

        return true;
    }
};

int main()
{
    int n;
    // 循环读取多组测试用例
    while (cin >> n)
    {
        vector<int> nums(n);
        // 读取数组元素
        for (int i = 0; i < n; ++i)
        {
            cin >> nums[i];
        }

        Solution solution;
        // 输出结果
        if (solution.isJolly(n, nums))
        {
            cout << "Jolly" << endl;
        }
        else
        {
            cout << "Not jolly" << endl;
        }
    }

    return 0;
}
