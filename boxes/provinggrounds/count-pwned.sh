#!/bin/bash
count=$(find . -maxdepth 1 -name '*.pwned' -type d | wc -l)
echo "$count/30 boxes pwned"
