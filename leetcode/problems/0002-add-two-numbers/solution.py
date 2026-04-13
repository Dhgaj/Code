# 2. 两数相加

# 给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。
# 请你将两个数相加，并以相同形式返回一个表示和的链表。
# 你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

# 示例 1：
# 输入：l1 = [2,4,3], l2 = [5,6,4]
# 输出：[7,0,8]
# 解释：342 + 465 = 807.

# 示例 2：
# 输入：l1 = [0], l2 = [0]
# 输出：[0]

# 示例 3：
# 输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
# 输出：[8,9,9,9,0,0,0,1]

# 定义链表节点
from typing import Optional


class ListNode:
    # 初始化节点
    def __init__(self, val=0, next=None):
        # 节点值
        self.val = val
        # 指向下一个节点
        self.next = next

# @lc code=start
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # 头指针
        dummy = ListNode(0)
        # 当前指针
        cur = dummy
        # 初始进位为 0
        carry = 0
        # 当有链表不为空时或有进位时循环
        while l1 or l2 or carry:
            # 取当前指针所指的链表值，为空则值为 0
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            # 计算和
            total = v1 + v2 + carry
            # 计算进位
            carry = total // 10
            # 写入 cur 的下一个节点
            cur.next = ListNode(total % 10)
            # 指向当前节点
            cur = cur.next
            # 继续链表的下一个节点
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        # 返回去除 dummy 头节点的链表
        return dummy.next
# @lc code=end

# 工具函数：list -> 链表
def build_list(arr):
    dummy = ListNode(0)
    cur = dummy
    for x in arr:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next


# 工具函数：链表 -> list
def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res


solution = Solution()

# 自动转换输入
l1 = build_list([2, 4, 3])
l2 = build_list([5, 6, 4])

# 调用
res = solution.addTwoNumbers(l1, l2)
# print(res) # 返回链表地址

# 转回 list 输出
print(to_list(res))
