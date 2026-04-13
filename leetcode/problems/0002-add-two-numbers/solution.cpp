// 2. 两数相加

// 给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。
// 请你将两个数相加，并以相同形式返回一个表示和的链表。
// 你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

// 示例 1：
// 输入：l1 = [2,4,3], l2 = [5,6,4]
// 输出：[7,0,8]
// 解释：342 + 465 = 807.

// 示例 2：
// 输入：l1 = [0], l2 = [0]
// 输出：[0]

// 示例 3：
// 输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
// 输出：[8,9,9,9,0,0,0,1]

#include <iostream>
using namespace std;

struct ListNode
{
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

// @lc code=start
class Solution
{
public:
    ListNode *addTwoNumbers(ListNode *l1, ListNode *l2)
    {
        struct ListNode dummy;
        dummy.next = NULL;
        struct ListNode *cur = &dummy;
        int sum=0;
        while (l1 || l2 || sum>0)
        {
            if (l1)
            {
                sum+=l1->val;
                l1 = l1->next;
            }
            if (l2)
            {
                sum+=l2->val;
                l2 = l2->next;
            }

            ListNode *node = new ListNode(sum % 10);
            node->next = NULL;

            sum /=10;

            cur->next = node;
            cur = node;

        }

        return dummy.next;
    }
};
// @lc code=end

// 构建链表
ListNode *buildList(int arr[], int size)
{
    ListNode dummy(0);
    ListNode *cur = &dummy;

    for (int i = 0; i < size; i++)
    {
        ListNode *node = new ListNode(arr[i]);
        cur->next = node;
        cur = cur->next;
    }

    return dummy.next;
}

// 打印链表
void printList(ListNode *head)
{
    cout << "[";

    while (head)
    {
        cout << head->val;
        if (head->next)
            cout << ",";
        head = head->next;
    }

    cout << "]" << endl;
}

// 主函数
int main()
{
    int a1[] = {2, 4, 3};
    int a2[] = {5, 6, 4};

    ListNode *l1 = buildList(a1, 3);
    ListNode *l2 = buildList(a2, 3);

    // 创建对象
    Solution s;
    ListNode *result = s.addTwoNumbers(l1, l2);

    printList(result);

    return 0;
}