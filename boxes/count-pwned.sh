#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

cd "$(dirname "$0")" || exit 1

folders=(*/)

report() {
    local label="$1" color="$2" find_expr="$3"
    local total=0
    for dir in "${folders[@]}"; do
        dir="${dir%/}"
        local list count
        list=$(eval find "\"$dir\"" -maxdepth 1 -mindepth 1 -type d $find_expr | sed "s|^$dir/||" | sort)
        if [[ -z "$list" ]]; then
            count=0
        else
            count=$(echo "$list" | wc -l)
        fi
        total=$((total + count))
        echo -e "  ${color}[$dir]${NC} $count $label"
        if [ "$count" -gt 0 ]; then
            echo "$list" | sed 's/^/    -> /'
        fi
    done
    echo -e "${BOLD}${color}[=] $total total $label${NC}"
    echo
}

report "pwned" "$GREEN" "-name '*.pwned'"
report "stuck" "$RED" "-name '*.stuck'"
report "not complete" "$YELLOW" "! -name '.*' ! -name '*.*'"
