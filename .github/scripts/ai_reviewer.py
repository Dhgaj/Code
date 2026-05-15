import os
import requests
import sys

def get_cloudflare_ai_response(code, filename):
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
    
    if not account_id or not api_token:
        print("⚠️ 未配置 CLOUDFLARE_API_TOKEN 或 CLOUDFLARE_ACCOUNT_ID，跳过 AI 分析。")
        return None

    # 默认使用目前 8B 级别中最强的 Llama 3.1 8B Instruct 模型，逻辑推理极佳
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-8b-instruct"
    
    prompt = f"""你是一个顶级的算法竞赛教练。请分析以下提交的算法代码（路径：{filename}）。
请严格按以下结构输出你的分析报告：
1. **代码审查**：指出代码中是否存在边界条件未处理、潜在的 Bug 或是不优雅的写法。
2. **复杂度分析**：评估当前代码的时间复杂度和空间复杂度。
3. **更优解法**：思考并详细说明是否有更优的数据结构或算法可以解决此题，并给出优化后的核心思路。

代码内容如下：
```
{code}
```
"""
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {"role": "system", "content": "你是一位专业的算法教练，熟知力扣(LeetCode)和洛谷的算法题解体系。"},
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
    changed_files_str = os.environ.get("CHANGED_FILES", "").strip()
    if not changed_files_str:
        print("ℹ️ 没有检测到需要审查的算法文件。")
        return

    changed_files = changed_files_str.split()
    
    for file_path in changed_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"🔍 正在审查文件: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        # 跳过空文件
        if not code.strip():
            print("ℹ️ 文件为空，跳过。")
            continue
            
        # 截取过长的代码，避免超出大模型的 Token 限制
        if len(code) > 8000:
            code = code[:8000] + "\n...[代码过长被截断]..."
            
        ai_report = get_cloudflare_ai_response(code, file_path)
        
        if ai_report:
            title = f"🤖 AI 算法审查: {os.path.basename(file_path)} [{file_path.split('/')[0].upper()}]"
            body = f"### 📄 文件路径：`{file_path}`\n\n{ai_report}\n\n---\n*由 Cloudflare Workers AI 自动生成的算法审查报告。*"
            create_github_issue(title, body)

if __name__ == "__main__":
    main()
