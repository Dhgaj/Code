// P1151 子数整数
// Author: Dhgaj
// Date: 2026-05-16

#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    // 返回所有符合条件的数
    vector<int> solve(int k)
    {
        // 存储答案
        vector<int> ans;

        // 在10000到30000的区间
        int minNum = 10000;
        int maxNum = 30000;

        // 遍历10000到30000
        for (int num = minNum; num <= maxNum; num++)
        {
            // 使用数学方法提取三个子数（极大降低字符串创建和截取的开销）
            int sub1 = num / 100;
            int sub2 = (num / 10) % 1000;
            int sub3 = num % 1000;

            // 判断是否符合条件
            if (sub1 % k == 0 && sub2 % k == 0 && sub3 % k == 0)
            {
                ans.push_back(num);
            }
        }

        return ans;
    }
};

int main()
{
    Solution solution;

    // 输入除数
    int k;
    cin >> k;

    // 调用核心逻辑
    vector<int> ans = solution.solve(k);

    // 如果没有找到
    if (ans.empty())
    {
        cout << "No" << endl;
    }
    else
    {
        // 输出答案
        for (int num : ans)
        {
            cout << num << endl;
        }
    }

    return 0;
}