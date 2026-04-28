#!/usr/bin/env bash

gcc -fPIC -shared -ldl -o ./libhax.so ./libhax.c

gcc -o ./rootshell ./rootshell.c
