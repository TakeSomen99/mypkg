#!/usr/bin/env python3
#SPDX-FileCopyrightText: 2025 TakeSomen99
#SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from device_msgs.srv import Device


def main():
    rclpy.init()
    node = Node("client")

    client = node.create_client(Device, "get_device_names")
    while not client.wait_for_service(timeout_sec=1.0):
        print("Waiting for service...")

    req = Device.Request()
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    print(future.result().names)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
