#!/bin/bash

# 根据 problems.txt 批量创建题目文件夹
# 用法: ./scripts/00-mkdir-dictionary.sh [leetcode|luogu|all]

# 获取项目根目录（脚本所在目录的上一级）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# 为指定平台创建题目文件夹
create_dirs_for_platform() {
    local platform="$1"
    local problems_file="$PROJECT_ROOT/$platform/problems.txt"
    local problems_dir="$PROJECT_ROOT/$platform/problems"

    # 检查 problems.txt 是否存在
    if [ ! -f "$problems_file" ]; then
        echo -e "${RED}错误: $problems_file 不存在${NC}"
        return 1
    fi

    # 确保 problems 目录存在
    mkdir -p "$problems_dir"

    echo -e "${BLUE}[$platform] 开始创建题目文件夹...${NC}"
    
    local created=0
    local skipped=0

    # 逐行读取 problems.txt
    while IFS= read -r line || [ -n "$line" ]; do
        # 跳过空行
        [ -z "$line" ] && continue
        
        local target_dir="$problems_dir/$line"
        
        if [ -d "$target_dir" ]; then
            # 目录已存在，跳过
            skipped=$((skipped + 1))
        else
            # 创建新目录
            mkdir -p "$target_dir"
            echo -e "  ${GREEN}✓ 创建: $line${NC}"
            created=$((created + 1))
        fi
    done < "$problems_file"

    echo -e "${BLUE}[$platform] 完成: 新建 ${created} 个, 跳过 ${skipped} 个已存在目录${NC}"
    echo ""
}

# 主逻辑
main() {
    local platform="$1"
    
    # 异常退出清理保护
    cleanup_and_exit_00() {
        clear
        tput cvvis
        tput sgr0
        exit 0
    }
    trap cleanup_and_exit_00 SIGINT SIGTERM
    
    # 如果没有传参，交互式选择
    if [ -z "$platform" ]; then
        local msg=""
        while true; do
            local cols=$(tput cols)
            [ -z "$cols" ] && cols=80
            [ "$cols" -gt 100 ] && cols=100
            [ "$cols" -lt 40 ] && cols=40
            
            local CYAN_BOLD='\033[1;36m'
            local border_line=$(printf "%$((cols - 1))s" | tr ' ' '─')

            local output=""
            output+="${CYAN_BOLD}╭${border_line}${NC}\n"
            output+="${CYAN_BOLD}│${NC}  ${YELLOW}批量创建题目文件夹${NC}\n"
            output+="${CYAN_BOLD}│${NC}\n"
            output+="${CYAN_BOLD}│${NC}  ${GREEN}1.${NC} leetcode\n"
            output+="${CYAN_BOLD}│${NC}  ${GREEN}2.${NC} luogu\n"
            output+="${CYAN_BOLD}│${NC}  ${GREEN}3.${NC} 全部 (all)\n"
            output+="${CYAN_BOLD}│${NC}\n"
            output+="${CYAN_BOLD}╰${border_line}${NC}\n"
            
            clear
            tput cvvis
            echo -e "$output"

            # 错误提示回显位置
            if [ -n "$msg" ]; then
                echo -e "  ${YELLOW}➔ $msg${NC}"
            fi

            read -rp "❯ 请选择操作平台 (1/2/3): " choice
            msg=""

            case "$choice" in
                1) platform="leetcode"; break ;;
                2) platform="luogu"; break ;;
                3) platform="all"; break ;;
                *) msg="无效选择，请重新输入" ;;
            esac
        done
    fi

    echo ""
    # 根据选择创建
    case "$platform" in
        leetcode) create_dirs_for_platform "leetcode" ;;
        luogu) create_dirs_for_platform "luogu" ;;
        all)
            create_dirs_for_platform "leetcode"
            create_dirs_for_platform "luogu"
            ;;
        *)
            echo -e "${RED}无效平台: $platform${NC}"
            echo "用法: $0 [leetcode|luogu|all]"
            return 1
            ;;
    esac
}


main "$@"
