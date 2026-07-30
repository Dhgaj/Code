#!/bin/bash

# 编译并运行题解代码
# 用法: ./scripts/02-run-solution.sh <文件路径>
# 示例: ./scripts/02-run-solution.sh leetcode/problems/0003-longest-substring-without-repeating-characters/solution.c

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    echo -e "${CYAN}正在检测变动的文件...${NC}"
    cd "$PROJECT_ROOT" || exit 1
    
    # 兼容 macOS bash 3，使用 IFS 按换行读取
    IFS=$'\n'
    changed_files=($(git ls-files --others --modified --exclude-standard 2>/dev/null | grep -E '\.(c|cpp|py)$'))
    unset IFS
    
    if [ ${#changed_files[@]} -eq 1 ]; then
        FILE_PATH="${changed_files[0]}"
        echo -e "自动检测到变动的文件: ${GREEN}${FILE_PATH}${NC}"
        read -rp "❯ 是否运行此文件？(Y/n): " confirm
        if [[ -n "$confirm" && ! "$confirm" =~ ^[Yy]$ ]]; then
            echo -e "${RED}已取消运行。${NC}"
            exit 0
        fi
        echo ""
    elif [ ${#changed_files[@]} -gt 1 ]; then
        echo -e "检测到多个变动的文件："
        for (( i=0; i<${#changed_files[@]}; i++ )); do
            echo -e "  ${GREEN}$((i+1)).${NC} ${changed_files[$i]}"
        done
        read -rp "❯ 请输入序号选择，或直接拖拽/输入其他路径: " choice_or_path
        
        if [[ "$choice_or_path" =~ ^[0-9]+$ ]] && [ "$choice_or_path" -ge 1 ] && [ "$choice_or_path" -le "${#changed_files[@]}" ]; then
            FILE_PATH="${changed_files[$((choice_or_path-1))]}"
            echo ""
        elif [ -n "$choice_or_path" ]; then
            FILE_PATH=$(echo "$choice_or_path" | sed -e "s/^'//" -e "s/'$//" -e 's/^"//' -e 's/"$//' | xargs)
            echo ""
        else
            echo -e "${RED}已取消运行。${NC}"
            exit 0
        fi
    else
        echo -e "未检测到变动的代码文件。"
        echo -e "${CYAN}请输入要运行的题解文件路径 (支持拖拽文件到终端):${NC}"
        read -rp "❯ " user_input
        if [ -n "$user_input" ]; then
            FILE_PATH=$(echo "$user_input" | sed -e "s/^'//" -e "s/'$//" -e 's/^"//' -e 's/"$//' | xargs)
            echo ""
        else
            echo -e "${RED}错误: 请提供要运行的文件路径${NC}"
            exit 1
        fi
    fi
fi

# 处理相对路径和绝对路径
if [ -f "$FILE_PATH" ]; then
    FILE_PATH="$(cd "$(dirname "$FILE_PATH")" && pwd)/$(basename "$FILE_PATH")"
elif [ -f "$PROJECT_ROOT/$FILE_PATH" ]; then
    FILE_PATH="$PROJECT_ROOT/$FILE_PATH"
else
    echo -e "${RED}错误: 文件 '$FILE_PATH' 不存在${NC}"
    exit 1
fi

# 获取文件扩展名和所在目录
EXT="${FILE_PATH##*.}"
DIR_NAME=$(dirname "$FILE_PATH")
FILE_NAME=$(basename "$FILE_PATH")
BASE_NAME="${FILE_NAME%.*}"

# 进入文件所在目录执行
cd "$DIR_NAME" || exit 1

run_with_inputs() {
    local exec_cmd="$1"

    if [ ! -f "input.txt" ]; then
        echo "----------------------------------------"
        eval "$exec_cmd"
        echo -e "\n----------------------------------------"
        return
    fi
    
    # 检查是否有 === 分隔符
    if ! grep -qE '^===\s*.*\s*===\s*$' "input.txt"; then
        echo -e "${CYAN}[自动读取 input.txt 作为整体输入]${NC}"
        echo "----------------------------------------"
        eval "$exec_cmd" < "input.txt"
        echo -e "\n----------------------------------------"
        return
    fi
    
    local tmp_dir=$(mktemp -d)
    
    # 使用 awk 根据 === xxx === 分割输入
    awk -v out_dir="$tmp_dir" '
        /^===\s*.*\s*===\s*$/ {
            if (out) { close(out) }
            idx++
            case_name = $0
            gsub(/^===\s*|\s*===$/, "", case_name)
            name_file = out_dir "/" idx ".name"
            print case_name > name_file
            close(name_file)
            
            out = out_dir "/" idx ".txt"
            next
        }
        {
            if (out) {
                print > out
            }
        }
    ' "input.txt"
    
    local count=0
    # 按照切分的序号顺序执行
    for name_file in $(ls -1 "$tmp_dir"/*.name 2>/dev/null | sort -V); do
        count=$((count+1))
        local base_idx=$(basename "$name_file" .name)
        local test_file="$tmp_dir/$base_idx.txt"
        local case_name=$(cat "$name_file")
        
        echo -e "${CYAN}[运行测试用例: ${case_name}]${NC}"
        echo "----------------------------------------"
        if [ -f "$test_file" ]; then
            eval "$exec_cmd" < "$test_file"
        else
            eval "$exec_cmd" < /dev/null
        fi
        echo -e "\n----------------------------------------"
    done
    
    if [ "$count" -eq 0 ]; then
        # 兜底：如果 awk 没切分出任何用例
        echo -e "${CYAN}[自动读取 input.txt 作为整体输入]${NC}"
        echo "----------------------------------------"
        eval "$exec_cmd" < "input.txt"
        echo -e "\n----------------------------------------"
    fi

    rm -rf "$tmp_dir"
}

case "$EXT" in
    c)
        echo -e "${YELLOW}正在编译 $FILE_NAME (C)...${NC}"
        # 编译 C 文件
        gcc "$FILE_NAME" -o "$BASE_NAME"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}编译成功！开始运行：${NC}"
            run_with_inputs "\"./$BASE_NAME\""
            echo -e "${GREEN}运行结束。${NC}"
        else
            echo -e "${RED}编译失败，取消运行。${NC}"
        fi
        ;;
    cpp)
        echo -e "${YELLOW}正在编译 $FILE_NAME (C++)...${NC}"
        # 编译 C++ 文件
        g++ "$FILE_NAME" -o "$BASE_NAME"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}编译成功！开始运行：${NC}"
            run_with_inputs "\"./$BASE_NAME\""
            echo -e "${GREEN}运行结束。${NC}"
        else
            echo -e "${RED}编译失败，取消运行。${NC}"
        fi
        ;;
    py)
        echo -e "${GREEN}开始运行 Python 脚本 ${FILE_NAME}：${NC}"
        run_with_inputs "python3 \"$FILE_NAME\""
        echo -e "${GREEN}运行结束。${NC}"
        ;;
    *)
        echo -e "${RED}错误: 不支持的文件类型 '.$EXT'，目前仅支持 .c, .cpp, .py${NC}"
        exit 1
        ;;
esac
