#!/bin/bash

# Code 项目主入口脚本
# 提供交互式菜单，选择执行不同的功能脚本

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
CYAN_BOLD='\033[1;36m'
BOLD='\033[1m'
NC='\033[0m'

# 显示主菜单
show_menu() {
    local cols=$(tput cols)
    [ -z "$cols" ] && cols=80
    [ "$cols" -gt 100 ] && cols=100
    [ "$cols" -lt 40 ] && cols=40

    local border_line=$(printf "%$((cols - 1))s" | tr ' ' '─')

    echo -e "${CYAN_BOLD}╭${border_line}${NC}"
    echo -e "${CYAN_BOLD}│${NC}  ${YELLOW}刷题管理工具${NC}"
    echo -e "${CYAN_BOLD}│${NC}"
    echo -e "${CYAN_BOLD}│${NC}  ${GREEN}1.${NC} 创建题解文件 (solution.c / .cpp / .py)"
    echo -e "${CYAN_BOLD}│${NC}  ${GREEN}2.${NC} 创建题目文件夹 (根据 problems.txt)"
    echo -e "${CYAN_BOLD}│${NC}  ${RED}0.${NC} 退出"
    echo -e "${CYAN_BOLD}│${NC}"
    # 底边框和上边框复用同一长度，保证菜单盒子的上下边严格对齐。
    echo -e "${CYAN_BOLD}╰${border_line}${NC}"
}

# 异常退出清理保护
cleanup_and_exit() {
    clear
    tput cvvis # 恢复可能被隐藏的光标
    tput sgr0  # 重置控制台颜色
    echo -e "${GREEN}Good Bye!${NC}"
    exit 0
}

# 注册中断信号捕获
trap cleanup_and_exit SIGINT SIGTERM

# 主循环
main() {
    local msg=""
    while true; do
        clear
        tput cvvis
        show_menu
        
        # 将提示信息打印在划线之下
        if [ -n "$msg" ]; then
            echo -e "  ${YELLOW}➔ $msg${NC}"
        fi

        # 在底层原生调用输入
        read -rp "❯ 请输入操作指令 (0/1/2): " choice


        # 重置提示信息
        msg=""

        case "$choice" in
            1)
                clear # 交出屏幕控制权
                bash "$SCRIPTS_DIR/01-create-solution.sh"
                ret=$?
                if [ "$ret" -eq 0 ]; then
                    echo -e "\n${YELLOW}任务执行完毕，按回车键返回...${NC}"
                    read -r
                fi
                ;;
            2)
                clear
                bash "$SCRIPTS_DIR/00-mkdir-dictionary.sh"
                ret=$?
                if [ "$ret" -eq 0 ]; then
                    echo -e "\n${YELLOW}任务执行完毕，按回车键返回...${NC}"
                    read -r
                fi
                ;;
            0)
                cleanup_and_exit
                ;;
            *)
                msg="无效选择，请重新输入"
                ;;
        esac
    done
}

main
