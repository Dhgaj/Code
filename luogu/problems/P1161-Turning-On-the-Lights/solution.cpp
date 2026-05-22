#include <iostream>
#include <vector>
using namespace std;

class Solution
{
public:
    int solve()
    {
        int n;
        cin >> n;

        vector<int> light(2000001, 0);

        double a;
        int t;
        for (int i = 0; i < n; i++)
        {
            cin >> a >> t;
            for (int j = 1; j <= t; j++)
            {
                int num = (int)(a * j);
                if (num >= 2000001) break;
                light[num]++;
            }
        }

        for (int i = 0; i < 2000001; i++)
        {
            if (light[i] % 2 == 1)
            {
                return i;
            }
        }

        return 0;
    }
};

int main()
{
    Solution solution;
    int answer = solution.solve();
    cout << answer;
    return 0;
}
