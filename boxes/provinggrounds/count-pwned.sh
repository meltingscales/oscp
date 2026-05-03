#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Total target boxes
TOTAL=30

# 1. Pwned Boxes
pwned_list=$(find . -maxdepth 1 -name '*.pwned' -type d | sed 's|^\./||' | sort)
if [[ -z "$pwned_list" ]]; then
    pwned_count=0
else
    pwned_count=$(echo "$pwned_list" | wc -l)
fi

percent=$((pwned_count * 100 / TOTAL))
echo -e "${GREEN}[+]${NC} $pwned_count/$TOTAL boxes pwned ($percent%)"

# 2. Stuck Boxes
stuck_list=$(find . -maxdepth 1 -name '*.stuck' -type d | sed 's|^\./||' | sort)
if [[ -z "$stuck_list" ]]; then
    stuck_count=0
else
    stuck_count=$(echo "$stuck_list" | wc -l)
fi

echo -e "${RED}[-]${NC} $stuck_count boxes stuck on"
if [ "$stuck_count" -gt 0 ]; then
    echo "$stuck_list" | sed 's/^/  -> /'
fi

# 3. Non-Completed Boxes (Directories with no extensions)
noncompleted_list=$(find . -maxdepth 1 -mindepth 1 -type d ! -name '.*' ! -name '*.*' | sed 's|^\./||' | sort)
if [[ -z "$noncompleted_list" ]]; then
    noncompleted_count=0
else
    noncompleted_count=$(echo "$noncompleted_list" | wc -l)
fi

echo -e "${YELLOW}[?]${NC} $noncompleted_count boxes not complete"
if [ "$noncompleted_count" -gt 0 ]; then
    echo "$noncompleted_list" | sed 's/^/  -> /'
fi
