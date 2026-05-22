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
1. **忽略工程规范**：不要指出缺少异常捕获(try-except)、scanf返回值检查、变量命名等工程规范问题。算法题只关注逻辑、边界、时空效率！
2. **完美代码免输出**：如果代码逻辑已经是非常完美的顶级解法，直接给予夸奖即可，**绝对不需要强行输出代码**。
3. **按需提供多语言优化**：如果代码**存在优化空间**，且用户同时提交了多种语言的代码（如 .c, .cpp, .py），你必须为**有改进空间的每一种语言**都分别提供独立的完整优化代码。
4. **代码输出格式（极其重要）**：为了能够实现自动化提取，如果你需要输出优化后的代码，**必须严格使用 XML 标签将其包裹，并标明原始文件的路径**。绝对不要使用普通的 markdown 代码块。格式必须严格如下：
<file path="原始文件的绝对路径">
这里写优化后的完整代码...
</file>
例如：
<file path="luogu/problems/P1151-Subnumber-Integer/solution.cpp">
#include <iostream>
using namespace std;
// ...
</file>

请按以下结构输出报告：
1. 🐛 **Bug 与逻辑陷阱**：指出会导致 WA 或 TLE 的错误。如果没有，写“无”。
2. ⏱️ **复杂度评估**：评估时间和空间复杂度。
3. 💡 **优化建议与代码**：说明更优思路。若代码已是最优，直接表扬；若有优化空间，务必按上述 XML `<file>` 标签格式输出所有语言的代码。

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
            {"role": "system", "content": "你是一位专业的算法竞赛教练。专注算法逻辑优化，无视工程规范。如果有代码输出，必须严格使用用户要求的 XML <file> 标签包裹，绝对不要使用普通的 Markdown 代码块。"},
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

def format_xml_to_markdown(text):
    # 局部导入 re 模块，确保正则可用
    import re
    # 正则匹配 AI 输出的自定义 XML 文件标签，并进行引号及尾部空格的高鲁棒性容错
    pattern = r'<file\s+path=["\']([^"\']+)["\']\s*>\s*(.*?)\s*</file>'
    
    def replace_match(match):
        # 获取匹配出的文件路径和优化代码内容
        file_path = match.group(1)
        code_content = match.group(2)
        
        # 提取文件后缀并将其映射为 Markdown 代码块的语言标识
        ext = os.path.splitext(file_path)[1].lower()
        lang_map = {
            ".py": "python",
            ".cpp": "cpp",
            ".java": "java",
            ".go": "go",
            ".c": "c",
            ".js": "javascript",
            ".ts": "typescript"
        }
        lang = lang_map.get(ext, "")
        
        # 清除代码内容首尾的多余空白字符
        code_content = code_content.strip()
        
        # 防御性逻辑：防止 AI 在 XML 内部依旧使用 Markdown 代码块进行包裹
        if code_content.startswith("```"):
            code_content = code_content.split("\n", 1)[-1]
        if code_content.endswith("```"):
            code_content = code_content.rsplit("```", 1)[0]
        code_content = code_content.strip()
            
        # 返回格式化后的 Markdown 代码块
        return f"\n\n**📁 优化后的代码 ({file_path})：**\n```{lang}\n{code_content}\n```\n"

    # 执行正则替换，并使用 DOTALL 标记支持匹配换行符
    return re.sub(pattern, replace_match, text, flags=re.DOTALL)

def extract_header_comments(original_code, file_path):
    # 根据文件类型确定单行注释的标记
    ext = os.path.splitext(file_path)[1].lower()
    
    # 获取原始代码的所有行
    lines = original_code.splitlines(keepends=True)
    header_lines = []
    
    in_block_comment = False
    block_comment_end_char = ""
    
    for line in lines:
        stripped = line.strip()
        
        # 如果当前在块注释内部
        if in_block_comment:
            header_lines.append(line)
            if block_comment_end_char in stripped:
                in_block_comment = False
            continue
            
        # 允许空白行作为头部的一部分
        if not stripped:
            header_lines.append(line)
            continue
            
        # 检查是否是单行注释
        if ext in [".cpp", ".c", ".java", ".go"]:
            if stripped.startswith("//"):
                header_lines.append(line)
                continue
            elif stripped.startswith("/*"):
                header_lines.append(line)
                if "*/" not in stripped:
                    in_block_comment = True
                    block_comment_end_char = "*/"
                continue
        elif ext == ".py":
            if stripped.startswith("#"):
                header_lines.append(line)
                continue
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                header_lines.append(line)
                # 检查是否在同一行结束了三引号注释
                quote_char = '"""' if stripped.startswith('"""') else "'''"
                # 排除只有这三个引号本身的情况，或者首尾都有的情况
                if stripped.count(quote_char) < 2:
                    in_block_comment = True
                    block_comment_end_char = quote_char
                continue
                
        # 一旦遇到既不是注释也不是空白的行，立即终止提取
        break
        
    return "".join(header_lines)

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
            # 将 AI 报告中的自定义 XML 代码标签格式化为漂亮的 Markdown 代码块
            formatted_report = format_xml_to_markdown(ai_report)
            body = f"### 📄 题目涉及文件：\n{files_list}\n\n{formatted_report}\n\n---\n*由 Cloudflare Workers AI 自动生成的算法审查报告。*"
            
            # 调用 GitHub API 创建合并后的 Issue
            create_github_issue(title, body)
            
            # --- 新增：解析 AI 输出的代码并覆盖本地文件，以便后续 GitHub Action 发起 PR ---
            import re
            # 正则表达式匹配：<file path="路径">代码</file>，并进行引号与空格的容错
            pattern = r'<file\s+path=["\']([^"\']+)["\']\s*>\s*(.*?)\s*</file>'
            matches = re.findall(pattern, ai_report, re.DOTALL)
            
            if matches:
                print(f"📦 发现了 {len(matches)} 份优化代码，准备覆盖本地文件并触发 PR...")
                for path, new_code in matches:
                    path = path.strip()
                    new_code = new_code.strip()
                    
                    # 防御性编程：防止 AI 在 XML 内部依旧手痒加了 ```python 等 Markdown 框
                    if new_code.startswith("```"):
                        new_code = new_code.split("\n", 1)[-1]
                    if new_code.endswith("```"):
                        new_code = new_code.rsplit("```", 1)[0]
                        
                    new_code = new_code.strip() + "\n"
                    # 安全校验：确保 AI 输出的路径确实是本次被修改的文件之一，防止被覆盖无关文件
                    if path in files:
                        try:
                            # 1. 尝试读取原文件的原始代码，以提取并保留原本的头部注释（如作者、题目、日期等元信息）
                            original_code = ""
                            if os.path.exists(path):
                                with open(path, "r", encoding="utf-8") as f:
                                    original_code = f.read()
                            
                            # 2. 提取头部注释
                            header_comments = extract_header_comments(original_code, path)
                            
                            # 3. 如果提取到了头部注释，将其格式化拼接在优化后代码的头部
                            if header_comments:
                                if not header_comments.endswith("\n\n"):
                                    header_comments = header_comments.rstrip() + "\n\n"
                                # 将头部注释与新代码合并，并去除新代码可能有的多余前导空格/换行
                                write_code = header_comments + new_code.lstrip()
                            else:
                                write_code = new_code
                                
                            # 4. 写入合并后的代码，覆盖本地文件
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(write_code)
                            print(f"✅ 已成功将优化代码覆盖写入本地准备提 PR：{path}")
                        except Exception as e:
                            print(f"❌ 覆盖写入本地文件 {path} 失败: {e}")
                    else:
                        print(f"⚠️ 忽略非法路径或不在本次审查范围内的文件：{path}")

if __name__ == "__main__":
    main()
