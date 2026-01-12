#!/usr/bin/bash
# SPDX-FileCopyrightText: 2025 TakeSomen99
# SPDX-License-Identifier: BSD-3-Clause

set -e

WS_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$WS_DIR"

echo "[1] colcon build test"
colcon build --cmake-args -DBUILD_TESTING=OFF
source install/setup.bash

echo "[2] launch test"
ros2 launch mypkg talk_listen.launch.py > /tmp/mypkg.log 2>&1 &
LAUNCH_PID=$!

sleep 3

echo "[3] service existence test"
ros2 service list | grep -q "^/device$" || {
    echo "service not found"
    kill $LAUNCH_PID
    wait $LAUNCH_PID || true
    exit 1
}

sleep 2

echo "[4] service call test"
RESULT=$(timeout 5 ros2 service call /device device_msgs/srv/Device "{}" 2>&1) || {
    echo "service call failed or timeout"
    kill $LAUNCH_PID
    wait $LAUNCH_PID || true
    exit 1
}

echo "$RESULT" | grep -q "names=" || {
    echo "no valid response"
    echo "$RESULT"
    kill $LAUNCH_PID
    wait $LAUNCH_PID || true
    exit 1
}

kill $LAUNCH_PID
wait $LAUNCH_PID || true

echo "test was completed!!!"
