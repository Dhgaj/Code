// P1003 [NOIP 2011 提高组] 铺地毯
// Author: Dhgaj
// Date: 2026-04-19

#include <iostream>
#include <vector>
using namespace std;

// 定义一个地毯类
class Carpet
{
public:
    int a, b, g, k;

    // 初始化地毯
    Carpet(int a, int b, int g, int k)
    {
        this->a = a;
        this->b = b;
        this->g = g;
        this->k = k;
    }

    // 判断一个点是否在地毯内
    bool covers(int x, int y)
    {
        return (x >= a && x <= a + g &&
                y >= b && y <= b + k);
    }
};

int main()
{
    // 地毯数量
    int n;
    cin >> n;

    // 存储所有地毯
    vector<Carpet> carpets;

    // 读取每张地毯
    for (int i = 0; i < n; i++)
    {
        int a, b, g, k;
        cin >> a >> b >> g >> k;

        // 创建对象并加入容器
        carpets.emplace_back(a, b, g, k);
    }

    // 查询点
    int x, y;
    cin >> x >> y;

    // 倒序查找
    for (int i = n - 1; i >= 0; i--)
    {
        if (carpets[i].covers(x, y))
        {
            cout << i + 1 << endl;
            return 0;
        }
    }

    // 没找到
    cout << -1 << endl;

    return 0;
}