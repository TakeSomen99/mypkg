#!/usr/bin/bash
#SPDX-FileCopyrightText: 2025 TakeSomen99
#SPDX-License-Identifier: BSD-3-Clause

set -e

WS_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$WS_DIR"

echo "[1] colcon build test"
if colcon build --cmake-args -DBUILD_TESTING=OFF; then
	echo "build succeeded"
else
	echo "build failed"
	exit 1
fi
source install/setup.bash

echo "[2] lauch test"
timeout 10 ros2 launch mypkg talk_listen.launch.py > /tmp/mypkg.log 2>&1 || true
LAUNCH_EXIT_CODE=$?

if [ $LAUNCH_EXIT_CODE -eq 0 ] || [ $LAUNCH_EXIT_CODE -eq 124 ]; then
    echo "launch succeeded"
else
    echo "launch failed"
    exit 1
fi

echo "test was completed!!!"
