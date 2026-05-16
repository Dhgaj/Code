import os
import requests

def get_cloudflare_ai_response(code, problem_name):
    # 从环境变量中获取 Cloudflare 的配置
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
    
    # 检查是否配置了必要的环境变量，若没有则直接跳过后续操作
    if not account_id or not api_token:
        print("⚠️ 未配置 CLOUDFLARE_API_TOKEN 或 CLOUDFLARE_ACCOUNT_ID，跳过 AI 分析。")
        return None

    # 使用针对代码优化的最新版顶级大模型：Qwen 2.5 Coder 32B Instruct
    # 相比 8B 模型，32B 的推理能力有质的飞跃，且专门为代码生成调优，完美胜任算法教练
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/qwen/qwen2.5-coder-32b-instruct"
    
    # 重新设计的专业算法提示词工程
    prompt = f"""你是一个顶级的算法竞赛(ACM/LeetCode/Luogu)教练。请对以下属于【{problem_name}】的算法代码进行深度审查。

⚠️ **严格准则**（必须遵守）：
1. **忽略工程规范**：不要指出缺少异常捕获(try-except)、scanf返回值检查、变量命名(如sum等保留字)等工程级规范问题。算法题只关注逻辑正确性、边界条件、时间/空间效率！
2. **拒绝废话**：如果代码逻辑已经是最优且正确的，直接指出其优点即可，绝对不要强行找茬。
3. **必须提供代码**：无论你是修复了 Bug 还是提出了更优的算法（如把 O(N^2) 优化为 O(N)），你**都必须提供完整的优化后代码**，并加上中文注释。

请按以下结构输出报告：
1. 🐛 **Bug 与逻辑陷阱**：只指出会导致 Wrong Answer (WA) 或 Time Limit Exceeded (TLE) 的致命逻辑错误及边界条件。
2. ⏱️ **复杂度评估**：准确评估当前核心算法的时间复杂度和空间复杂度。
3. 💡 **更优解法与代码**：详细说明更优的解法思路，并**直接给出完整的优化代码**（使用 markdown 代码块）。

被审查的代码如下：
{code}
"""
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "max_tokens": 2048, # 增加最大 Token 数，防止 AI 的长篇分析和代码生成被半路截断
        "messages": [
            {"role": "system", "content": "你是一位专业的算法竞赛教练。你的职责是专注算法逻辑优化，无视工程规范，并且总是用 Markdown 代码块提供优化后的完整代码。"},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('result', {}).get('response')
    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"返回内容: {response.text}")
        return None

def create_github_issue(title, body):
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    
    if not repo or not token:
        print("⚠️ 缺少 GitHub 环境变量，无法创建 Issue。")
        return
        
    url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"title": title, "body": body}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ 成功创建 Issue: {response.json().get('html_url')}")
    else:
        print(f"❌ 创建 Issue 失败: {response.status_code} - {response.text}")

def main():
    # 获取环境变量中需要审查的文件列表字符串
    changed_files_str = os.environ.get("CHANGED_FILES", "").strip()
    # 如果没有文件变更，则直接结束
    if not changed_files_str:
        print("ℹ️ 没有检测到需要审查的算法文件。")
        return

    # 按空格拆分文件列表
    changed_files = changed_files_str.split()
    
    # 使用字典来按题目的文件夹对文件进行分组归类，实现同一题目合并审查
    from collections import defaultdict
    problems = defaultdict(list)
    
    for file_path in changed_files:
        # 确认文件真实存在后再加入处理队列
        if not os.path.exists(file_path):
            continue
        # 提取文件所在的文件夹路径作为同一题目的唯一标识
        dir_name = os.path.dirname(file_path)
        if not dir_name:
            dir_name = "未分类"
        problems[dir_name].append(file_path)
        
    # 遍历每个题目分组，将同一题目的多个文件合并成一次 AI 请求
    for problem_dir, files in problems.items():
        print(f"🔍 正在审查题目分组: {problem_dir} (包含 {len(files)} 个文件)")
        
        problem_code_blocks = []
        for file_path in files:
            # 读取当前文件的内容
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            # 如果文件为空，直接跳过
            if not code.strip():
                continue
            # 将每个文件的名字和代码内容拼接在一起，方便 AI 区分理解
            problem_code_blocks.append(f"### 文件：{file_path}\n```\n{code}\n```")
            
        # 如果该题目的所有文件均为空，则无需请求 AI
        if not problem_code_blocks:
            print(f"ℹ️ {problem_dir} 下全为空文件，跳过。")
            continue
            
        # 将该题目的所有代码块合并为一个连续的代码字符串
        combined_code = "\n\n".join(problem_code_blocks)
        
        # 为了防止传入的代码过长超出 AI 模型的处理上限，做截断处理
        if len(combined_code) > 8000:
            combined_code = combined_code[:8000] + "\n...[代码过长被截断]..."
            
        # 将合并后的代码整体发给 AI 导师获取审查报告
        ai_report = get_cloudflare_ai_response(combined_code, problem_dir)
        
        if ai_report:
            # 获取题目所在的平台
            platform = problem_dir.split('/')[0].upper() if '/' in problem_dir else "算法题"
            # 提取具体的题目名
            problem_basename = os.path.basename(problem_dir)
            
            # 生成合并后的 Issue 标题
            title = f"🤖 AI 算法审查: {problem_basename} [{platform}]"
            
            # 在 Issue 内容中列出所有的被审查的文件
            files_list = "\n".join([f"- `{f}`" for f in files])
            body = f"### 📄 题目涉及文件：\n{files_list}\n\n{ai_report}\n\n---\n*由 Cloudflare Workers AI 自动生成的算法审查报告。*"
            
            # 调用 GitHub API 创建合并后的 Issue
            create_github_issue(title, body)

if __name__ == "__main__":
    main()
