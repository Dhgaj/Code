// P1151 子数整数
// Author: Dhgaj
// Date: 2026-05-16

#include <iostream>
#include <vector>
#include <string>
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
            // 转化为字符串
            string s = to_string(num);

            // 存储连续三个数字
            vector<int> result;

            // 取123、234、345
            for (int i = 0; i < s.size() - 2; i++)
            {
                // 截取长度为3的子串并转成整数
                int value = stoi(s.substr(i, 3));

                result.push_back(value);
            }

            // 判断是否符合条件
            if (result[0] % k == 0 &&
                result[1] % k == 0 &&
                result[2] % k == 0)
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