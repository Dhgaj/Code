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

#include <stdio.h>
#include <stdlib.h>

struct ListNode
{
    int val;
    struct ListNode *next;
};

// @lc code=start
struct ListNode *addTwoNumbers(struct ListNode *l1, struct ListNode *l2)
{
    // 头节点
    struct ListNode dummy;
    dummy.next = NULL;
    // 头指针
    struct ListNode *cur = &dummy;
    int sum = 0;
    
    // 不为空时计算节点值和进位之和
    while (l1 || l2 || (sum > 0))
    {
        if (l1)
        {
            sum += l1->val;
            l1 = l1->next;
        }
        if (l2)
        {
            sum += l2->val;
            l2 = l2->next;
        }

        // malloc 创建节点存放值
        struct ListNode *node = malloc(sizeof(struct ListNode));
        node->val = sum % 10;
        node->next = NULL;

        // 存进位值
        sum /= 10;

        // 加入到链表中
        cur->next = node;
        cur = cur->next;
    }

    return dummy.next;
}
// @lc code=end

struct ListNode *buildList(int arr[], int size)
{
    struct ListNode dummy;
    dummy.next = NULL;

    struct ListNode *cur = &dummy;

    for (int i = 0; i < size; i++)
    {
        struct ListNode *node = malloc(sizeof(struct ListNode));
        node->val = arr[i];
        node->next = NULL;

        cur->next = node;
        cur = cur->next;
    }

    return dummy.next;
}

void printList(struct ListNode *head)
{
    printf("[");

    while (head)
    {
        printf("%d", head->val);

        if (head->next)
            printf(",");

        head = head->next;
    }

    printf("]\n");
}

int main()
{
    int a1[] = {2, 4, 3};
    int a2[] = {5, 6, 4};

    struct ListNode *l1 = buildList(a1, 3);
    struct ListNode *l2 = buildList(a2, 3);

    struct ListNode *result = addTwoNumbers(l1, l2);

    printList(result);

    return 0;
}