#!/bin/bash

# 在指定题目目录下创建题解文件 (solution.c / solution.cpp / solution.py)
# 用法: ./scripts/01-create-solution.sh [题号] [语言...]
# 示例: ./scripts/01-create-solution.sh 0001
#        ./scripts/01-create-solution.sh P1000 c py

# 获取项目根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 支持的语言列表
ALL_LANGS=("c" "cpp" "py")

# 生成 solution.c 模板
generate_c_template() {
    local problem_name="$1"
    cat << 'EOF'
// PROBLEM_NAME
// Author:
// Date:

#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // TODO: 实现逻辑
    return 0;
}
EOF
}

# 生成 solution.cpp 模板
generate_cpp_template() {
    local problem_name="$1"
    cat << 'EOF'
// PROBLEM_NAME
// Author:
// Date:

#include <iostream>
#include <vector>
using namespace std;

int main() {
    // TODO: 实现逻辑
    return 0;
}
EOF
}

# 生成 solution.py 模板
generate_py_template() {
    local problem_name="$1"
    cat << 'EOF'
# PROBLEM_NAME
# Author:
# Date:

def main():
    # TODO: 实现逻辑
    pass

if __name__ == "__main__":
    main()
EOF
}

# 将用户输入的编号标准化（支持纯数字、带前缀等多种格式）
# 例如: 3 → 0003, 0003 → 0003, P1000 → P1000
normalize_id() {
    local input="$1"
    local platform="$2"

    # 如果输入已经包含 "-"（如 0003-longest-xxx），直接用作前缀匹配
    if [[ "$input" == *-* ]]; then
        echo "$input"
        return
    fi

    # leetcode: 纯数字补零到4位
    if [ "$platform" = "leetcode" ]; then
        # 去掉前导零后再补齐4位
        local num
        num=$(echo "$input" | sed 's/^0*//')
        [ -z "$num" ] && num="0"
        printf "%04d" "$num"
    else
        # luogu: 原样返回（如 P1000）
        echo "$input"
    fi
}

# 根据题号前缀模糊匹配目录名
find_problem_dir() {
    local platform="$1"
    local problem_id="$2"
    local problems_dir="$PROJECT_ROOT/$platform/problems"

    # 标准化编号
    local normalized_id
    normalized_id=$(normalize_id "$problem_id" "$platform")

    # 在 problems 目录中查找匹配的目录
    local matched_dir=""
    local match_count=0

    for dir in "$problems_dir"/*/; do
        local dirname
        dirname="$(basename "$dir")"
        
        # 不区分大小写匹配（兼容 macOS bash）
        local lower_dirname
        lower_dirname=$(echo "$dirname" | tr '[:upper:]' '[:lower:]')
        local lower_id
        lower_id=$(echo "$normalized_id" | tr '[:upper:]' '[:lower:]')

        # 前缀匹配：目录名以标准化编号开头
        if [[ "$lower_dirname" == "$lower_id"* ]]; then
            matched_dir="$dirname"
            match_count=$((match_count + 1))
        fi
    done

    if [ "$match_count" -eq 0 ]; then
        echo ""
        return 1
    elif [ "$match_count" -eq 1 ]; then
        echo "$matched_dir"
        return 0
    else
        # 多个匹配，优先精确匹配（编号-名称完全一致）
        for dir in "$problems_dir"/*/; do
            local dirname
            dirname="$(basename "$dir")"
            local lower_dirname
            lower_dirname=$(echo "$dirname" | tr '[:upper:]' '[:lower:]')
            local lower_id
            lower_id=$(echo "$normalized_id" | tr '[:upper:]' '[:lower:]')
            if [[ "$lower_dirname" == "$lower_id" ]]; then
                echo "$dirname"
                return 0
            fi
        done
        # 优先匹配 "编号-" 格式（精确到编号部分）
        for dir in "$problems_dir"/*/; do
            local dirname
            dirname="$(basename "$dir")"
            local lower_dirname
            lower_dirname=$(echo "$dirname" | tr '[:upper:]' '[:lower:]')
            local lower_id
            lower_id=$(echo "$normalized_id" | tr '[:upper:]' '[:lower:]')
            if [[ "$lower_dirname" == "${lower_id}-"* ]]; then
                echo "$dirname"
                return 0
            fi
        done
        # 返回第一个匹配
        echo "$matched_dir"
        return 0
    fi
}

# 在指定目录创建题解文件
create_solution_files() {
    local platform="$1"
    local target_dir="$2"
    local problem_name="$3"
    shift 3
    local langs=("$@")

    local created=0
    local skipped=0

    for lang in "${langs[@]}"; do
        local filename="solution.$lang"
        local filepath="$target_dir/$filename"

        if [ -f "$filepath" ]; then
            echo -e "  ${YELLOW}⚠ 已存在: $filename (跳过)${NC}"
            skipped=$((skipped + 1))
            continue
        fi

        # 根据语言生成对应模板，并替换题目名称
        case "$lang" in
            c)
                if [ "$platform" = "leetcode" ]; then
                    echo "// $problem_name" > "$filepath"
                else
                    generate_c_template "$problem_name" | sed "s/PROBLEM_NAME/$problem_name/g" > "$filepath"
                fi
                ;;
            cpp)
                if [ "$platform" = "leetcode" ]; then
                    echo "// $problem_name" > "$filepath"
                else
                    generate_cpp_template "$problem_name" | sed "s/PROBLEM_NAME/$problem_name/g" > "$filepath"
                fi
                ;;
            py)
                if [ "$platform" = "leetcode" ]; then
                    echo "# $problem_name" > "$filepath"
                else
                    generate_py_template "$problem_name" | sed "s/PROBLEM_NAME/$problem_name/g" > "$filepath"
                fi
                ;;
        esac

        echo -e "  ${GREEN}✓ 创建: $filename${NC} -> $target_dir"
        created=$((created + 1))
    done

    echo ""
    echo -e "${BLUE}完成: 新建 ${created} 个文件, 跳过 ${skipped} 个已存在文件${NC}"
}

# 全局待办数组
leetcode_arr=()
leetcode_miss=()
luogu_arr=()
luogu_miss=()

collect_problems() {
    local platform="$1"
    local problems_dir="$PROJECT_ROOT/$platform/problems"
    
    for dir in "$problems_dir"/*/; do
        [ -d "$dir" ] || continue
        local dirname
        dirname="$(basename "$dir")"

        # 检查是否三种文件都已存在（已完成则跳过）
        if [ -f "$dir/solution.c" ] && [ -f "$dir/solution.cpp" ] && [ -f "$dir/solution.py" ]; then
            continue
        fi

        # 显示缺少的文件类型
        local missing=""
        [ ! -f "$dir/solution.c" ] && missing="${missing} .c"
        [ ! -f "$dir/solution.cpp" ] && missing="${missing} .cpp"
        [ ! -f "$dir/solution.py" ] && missing="${missing} .py"

        if [ "$platform" = "leetcode" ]; then
            leetcode_arr+=("$dirname")
            leetcode_miss+=("$missing")
        else
            luogu_arr+=("$dirname")
            luogu_miss+=("$missing")
        fi
    done
}

# 主逻辑
main() {
    local problem_id="$1"
    shift 1 2>/dev/null
    local specified_langs=("$@")

    # 交互式输入题号
    if [ -z "$problem_id" ]; then
        collect_problems "leetcode"
        collect_problems "luogu"

        local lc_page=1
        local lg_page=1
        local page_size=8
        local total_lc=${#leetcode_arr[@]}
        local total_lg=${#luogu_arr[@]}

        local lc_pages=$(( (total_lc + page_size - 1) / page_size ))
        [ "$lc_pages" -eq 0 ] && lc_pages=1
        local lg_pages=$(( (total_lg + page_size - 1) / page_size ))
        [ "$lg_pages" -eq 0 ] && lg_pages=1

        # 异常退出清理保护
        cleanup_and_exit_01() {
            clear
            tput cvvis
            tput sgr0
            exit 0
        }
        trap cleanup_and_exit_01 SIGINT SIGTERM

        # local is_first_render=true
        local msg=""
        local input_parts=()

        # 开场准备
        clear
        tput cvvis

        # 开始流式复写交互循环
        while true; do
            local cols=$(tput cols)
            [ -z "$cols" ] && cols=80
            [ "$cols" -gt 100 ] && cols=100
            [ "$cols" -lt 40 ] && cols=40
            
            local CYAN_BOLD='\033[1;36m'
            # 所有边框和分隔线都统一改成纯横线，让长度只由终端列数控制，不再受中文显示宽度影响。
            local border_line=$(printf "%$((cols - 1))s" | tr ' ' '─')

            local output=""
            # 顶部先输出纯边框，再把页面标题放入内容区，彻底消除标题参与边框长度计算的问题。
            output+="${CYAN_BOLD}╭${border_line}${NC}\n"
            # 总标题单独占一行显示，这样中文标题不会再把顶部横线撑得长短不一。
            output+="${CYAN_BOLD}│${NC}  ${YELLOW}待办题目一览${NC}\n"
            output+="${CYAN_BOLD}│${NC}\n"
            
            # Leetcode 区块
            output+="${CYAN_BOLD}│${NC}  ${CYAN}[leetcode] 进度: ${total_lc} 题待办 (页 ${lc_page}/${lc_pages}):${NC}\n"
            local printed_lc=0
            if [ "$total_lc" -eq 0 ]; then
                output+="${CYAN_BOLD}│${NC}    ${GREEN}全部分支已创建题解文件！${NC}\n"
                printed_lc=1
            else
                local start_idx=$(( (lc_page - 1) * page_size ))
                local end_idx=$(( start_idx + page_size ))
                [ $end_idx -gt $total_lc ] && end_idx=$total_lc
                
                for (( i=start_idx; i<end_idx; i++ )); do
                    local line_str
                    printf -v line_str "    %-60s %b" "${leetcode_arr[$i]}" "${YELLOW}[缺少:${leetcode_miss[$i]}]${NC}"
                    output+="${CYAN_BOLD}│${NC}${line_str}\n"
                    printed_lc=$((printed_lc + 1))
                done
            fi
            # 补齐防抖动空行
            while [ "$printed_lc" -lt "$page_size" ]; do output+="${CYAN_BOLD}│${NC}\n"; printed_lc=$((printed_lc + 1)); done
            output+="${CYAN_BOLD}│${NC}\n"

            # Leetcode 与 Luogu 之间改成纯分隔线，不再显示 "Luogu 分区" 文本，和你的预期一致。
            output+="${CYAN_BOLD}├${border_line}${NC}\n"
            # 分隔线后保留一个空行，让上下两个分区的视觉留白保持一致。
            output+="${CYAN_BOLD}│${NC}\n"

            # Luogu 区块
            output+="${CYAN_BOLD}│${NC}  ${CYAN}[luogu] 进度: ${total_lg} 题待办 (页 ${lg_page}/${lg_pages}):${NC}\n"
            local printed_lg=0
            if [ "$total_lg" -eq 0 ]; then
                output+="${CYAN_BOLD}│${NC}    ${GREEN}全部分支已创建题解文件！${NC}\n"
                printed_lg=1
            else
                local start_idx=$(( (lg_page - 1) * page_size ))
                local end_idx=$(( start_idx + page_size ))
                [ $end_idx -gt $total_lg ] && end_idx=$total_lg
                
                for (( i=start_idx; i<end_idx; i++ )); do
                    local line_str
                    printf -v line_str "    %-60s %b" "${luogu_arr[$i]}" "${YELLOW}[缺少:${luogu_miss[$i]}]${NC}"
                    output+="${CYAN_BOLD}│${NC}${line_str}\n"
                    printed_lg=$((printed_lg + 1))
                done
            fi
            while [ "$printed_lg" -lt "$page_size" ]; do output+="${CYAN_BOLD}│${NC}\n"; printed_lg=$((printed_lg + 1)); done

            # Luogu 列表结束后先补一个空行，让下一个操作区与上方列表之间留出一致的间距。
            output+="${CYAN_BOLD}│${NC}\n"
            # 操作区前也改成纯分隔线，避免不同标题文字导致分隔线长度看起来不统一。
            output+="${CYAN_BOLD}├${border_line}${NC}\n"
            # 再补一个空行，把分隔线和具体提示内容分开，视觉上会更平整。
            output+="${CYAN_BOLD}│${NC}\n"
            output+="${CYAN_BOLD}│${NC}  ${CYAN}翻页指令: [n]/[p] 同时 | [nl]/[pl] lc | [ng]/[pg] lg | [q] 退出${NC}\n"
            if [ -n "$msg" ]; then
                output+="${CYAN_BOLD}│${NC}  ${YELLOW}➔ ${msg}${NC}\n"
            else
                output+="${CYAN_BOLD}│${NC}  ${YELLOW}提示: P开头识别为 luogu，否则为 leetcode。带语言如 'P1000 c cpp'${NC}\n"
            fi
            # 底边框复用同一条纯横线，这样顶部、分隔线、底部都会严格同宽。
            output+="${CYAN_BOLD}╰${border_line}${NC}\n"

            # 打印整个输出大纲
            clear
            tput cvvis
            echo -e "$output"

            # 原生态悬停输入
            read -rp "❯ 请输入题目编号 (如 3 或 P1000) 或翻页指令: " input_line
            msg=""
            
            # 处理指令
            local cmd
            cmd=$(echo "$input_line" | tr '[:upper:]' '[:lower:]')
            
            # 过滤纯回车，静默刷新
            if [ -z "$cmd" ]; then
                continue
            fi

            case "$cmd" in
                n)
                    [ "$lc_page" -lt "$lc_pages" ] && lc_page=$((lc_page + 1))
                    [ "$lg_page" -lt "$lg_pages" ] && lg_page=$((lg_page + 1))
                    continue ;;
                p)
                    [ "$lc_page" -gt 1 ] && lc_page=$((lc_page - 1))
                    [ "$lg_page" -gt 1 ] && lg_page=$((lg_page - 1))
                    continue ;;
                nl)
                    [ "$lc_page" -lt "$lc_pages" ] && lc_page=$((lc_page + 1))
                    continue ;;
                pl)
                    [ "$lc_page" -gt 1 ] && lc_page=$((lc_page - 1))
                    continue ;;
                ng)
                    [ "$lg_page" -lt "$lg_pages" ] && lg_page=$((lg_page + 1))
                    continue ;;
                pg)
                    [ "$lg_page" -gt 1 ] && lg_page=$((lg_page - 1))
                    continue ;;
                q|quit|exit)
                    return 2 ;;
            esac

            # 如果不属于快捷指令，我们将它按题号解析：第一个词是题号，后续是语言
            read -ra input_parts <<< "$input_line"
            problem_id="${input_parts[0]}"
            
            # (此时 problem_id 不可能为空，因前面已拦截 z "$cmd")


            # 跳出分页循环开始分配任务
            break
        done
        
        # 如果用户在输入中指定了语言
        if [ "${#input_parts[@]}" -gt 1 ]; then
            specified_langs=("${input_parts[@]:1}")
        fi
    fi

    # 自动判断平台
    local platform="leetcode"
    if [[ "$problem_id" == [pP]* ]]; then
        platform="luogu"
    fi

    # 检查平台目录是否存在
    local problems_dir="$PROJECT_ROOT/$platform/problems"
    if [ ! -d "$problems_dir" ]; then
        echo -e "${RED}错误: 平台目录 $problems_dir 不存在${NC}"
        return 1
    fi

    # 确定要生成的语言列表
    local langs=()
    if [ "${#specified_langs[@]}" -gt 0 ]; then
        # 验证用户指定的语言
        for lang in "${specified_langs[@]}"; do
            local valid=false
            for supported in "${ALL_LANGS[@]}"; do
                if [ "$lang" == "$supported" ]; then
                    valid=true
                    break
                fi
            done
            if $valid; then
                langs+=("$lang")
            else
                echo -e "${YELLOW}警告: 不支持的语言 '$lang'，已忽略 (支持: c, cpp, py)${NC}"
            fi
        done
        
        if [ "${#langs[@]}" -eq 0 ]; then
            echo -e "${RED}错误: 没有有效的语言指定${NC}"
            return 1
        fi
    else
        # 默认生成全部三种
        langs=("${ALL_LANGS[@]}")
    fi

    # 查找题目目录
    local dir_name
    dir_name=$(find_problem_dir "$platform" "$problem_id")
    
    if [ -z "$dir_name" ]; then
        echo -e "${RED}错误: 未找到编号为 '$problem_id' 的题目目录${NC}"
        echo -e "${YELLOW}提示: 请先运行功能 2 创建题目文件夹，或检查编号是否正确${NC}"
        return 1
    fi

    local target_dir="$problems_dir/$dir_name"
    echo -e "${BLUE}匹配到题目: ${GREEN}$dir_name${NC}"
    echo -e "${BLUE}生成语言: ${GREEN}${langs[*]}${NC}"
    echo ""

    # 创建文件
    create_solution_files "$platform" "$target_dir" "$dir_name" "${langs[@]}"
}

main "$@"
