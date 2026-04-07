#!/bin/bash

count=$(find . -maxdepth 1 -name '*.pwned' -type d | wc -l)
percent=$((count * 100 / 30))
echo "$count/30 boxes pwned ($percent%)"

stuck=$(find . -maxdepth 1 -name '*.stuck' -type d | wc -l)
echo "$stuck boxes stuck on"

noncompleted=$(find . -maxdepth 1 -mindepth 1 -type d ! -name '.*' ! -name '*.*' | wc -l)
echo "$noncompleted boxes not complete"
