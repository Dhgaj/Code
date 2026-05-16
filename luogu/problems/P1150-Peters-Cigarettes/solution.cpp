// P1150 Peter 的烟
// Author: Dhgaj
// Date: 2026-05-16

#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    int countTheSum(int n, int k, int sum)
    {
        while (n >= k)
        {
            // Peter手中剩余的烟
            n = n - k + 1;
            // 计算已经换取的烟蒂
            sum += k;
        }

        return sum + n;
    }
};

int main()
{
    // 吸烟有害健康，请诊视自己的身体 ！！！
    //  输入Peter有的n根烟和达到数量k能够换取的条件
    int n, k, sum;
    cin >> n >> k;
    sum = 0;

    Solution solution;
    int result = solution.countTheSum(n, k, sum);
    cout << result;

    return 0;
}
