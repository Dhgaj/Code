import os
import re

def count_problems(path):
    """统计指定路径下的题目数量（包含代码或 Markdown 文件的有效子目录）"""
    if not os.path.exists(path):
        return 0
    count = 0
    # 遍历 problems 下的每个子目录
    for d in os.listdir(path):
        d_path = os.path.join(path, d)
        # 排除隐藏文件、非文件夹以及以 test（不区分大小写）开头的文件夹
        if os.path.isdir(d_path) and not d.startswith('.') and not d.lower().startswith('test'):
            # 检查目录下是否包含 .cpp, .c, .py 或 .md 文件
            files = [f for f in os.listdir(d_path) if f.endswith(('.cpp', '.c', '.py', '.md'))]
            if files:
                count += 1
    return count

def update_readme():
    """更新 README.md 中的统计数据"""
    leetcode_count = count_problems('leetcode/problems')
    luogu_count = count_problems('luogu/problems')
    total_count = leetcode_count + luogu_count

    stats_table = f"""| 平台 | 已解决 | 状态 |
| :--- | :---: | :---: |
| **LeetCode** | {leetcode_count} | ⏳ 持续更新 |
| **Luogu** | {luogu_count} | ⏳ 持续更新 |
| **总计** | **{total_count}** | 🚀 保持奋进 |"""

    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print("未找到 README.md 文件")
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则替换 <!-- STATS_START --> 和 <!-- STATS_END --> 之间的内容
    pattern = r'<!-- STATS_START -->.*?<!-- STATS_END -->'
    replacement = f'<!-- STATS_START -->\n{stats_table}\n<!-- STATS_END -->'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"统计更新成功: LeetCode({leetcode_count}), Luogu({luogu_count})")

if __name__ == "__main__":
    # 切换到项目根目录执行（假设脚本在 .github/scripts/ 目录下，需要上跳三级）
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    update_readme()
