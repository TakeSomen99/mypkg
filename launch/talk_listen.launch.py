#!/usr/bin/env python3
#SPDX-FileCopyrightText: 2025 TakeSomen99
#SPDX-License-Identifier: BSD-3-Clause

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    server = Node(
        package='mypkg',
        executable='server',
        name='device_server',
        output='screen',
    )

    client = Node(
        package='mypkg',
        executable='client',
        name='device_client',
        output='screen',
    )

    return LaunchDescription([
        server,
        client,
    ])

