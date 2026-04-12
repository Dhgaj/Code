// 1.两数之和

// 给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。
// 你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。
// 你可以按任意顺序返回答案。

// 示例 1：
// 输入：nums = [2,7,11,15], target = 9
// 输出：[0,1]
// 解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。

// 示例 2：
// 输入：nums = [3,2,4], target = 6
// 输出：[1,2]

// 示例 3：
// 输入：nums = [3,3], target = 6
// 输出：[0,1]

#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // 定义哈希表：key = 数值，value = 下标
        unordered_map<int, int> map;

        // 遍历数组
        for (int i = 0; i < nums.size(); i++) {

            // 计算需要的另一个数
            int complement = target - nums[i];

            // 如果哈希表中存在这个数
            if (map.find(complement) != map.end()) {
                // 返回两个下标
                return {map[complement], i};
            }

            // 不存在则存入哈希表
            map[nums[i]] = i;
        }

        // 理论上不会走到这里
        return {};
    }
};

int main() {
    // 定义输入数组
    vector<int> nums = {2, 7, 11, 15};

    // 目标值
    int target = 9;

    // 创建对象
    Solution solution;

    // 调用函数
    vector<int> result = solution.twoSum(nums, target);

    // 输出结果
    cout << "结果下标: ";
    for (int index : result) {
        cout << index << " ";
    }
    cout << endl;

    return 0;
}