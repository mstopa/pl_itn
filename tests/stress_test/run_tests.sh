#!/bin/bash
locust --headless --skip-log --json --users 50 --spawn-rate 5 --run-time 10m -H http://localhost:8000 > 50users10min.json
locust --headless --skip-log --json --users 100 --spawn-rate 5 --run-time 10m -H http://localhost:8000 > 100users10min.json
locust --headless --skip-log --json --users 150 --spawn-rate 5 --run-time 10m -H http://localhost:8000 > 150users10min.json
locust --headless --skip-log --json --users 250 --spawn-rate 5 --run-time 10m -H http://localhost:8000 > 250users10min.json
locust --headless --skip-log --json --users 150 --spawn-rate 5 --run-time 60m -H http://localhost:8000 > 150users60min.json
