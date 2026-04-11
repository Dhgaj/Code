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

#include <stdio.h>
#include <stdlib.h>

/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {

    // 分配返回结果空间（两个下标）
    int* res = (int*)malloc(2 * sizeof(int));

    // 暴力枚举两数之和
    for (int i = 0; i < numsSize; i++) {
        for (int j = i + 1; j < numsSize; j++) {

            // 找到目标
            if (nums[i] + nums[j] == target) {
                res[0] = i;
                res[1] = j;

                // 返回结果大小 = 2
                *returnSize = 2;

                return res;
            }
        }
    }

    *returnSize = 0;
    return NULL;
}

int main() {
    // 测试数据
    int nums[] = {2, 7, 11, 15};
    int target = 9;
    int returnSize;

    int* result = twoSum(nums, 4, target, &returnSize);

    // 打印结果
    for (int i = 0; i < returnSize; i++) {
        printf("%d ", result[i]);
    }

    free(result);
    return 0;
}