#!/usr/bin/env bash

export HTB_IP=10.129.1.254

curl -X POST http://$HTB_IP:8080/api/login -d '{"username": "admin", "password": "password"}'
