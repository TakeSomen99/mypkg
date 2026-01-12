#!/usr/bin/env python3
#SPDX-FileCopyrightText: 2025 TakeSomen99
#SPDX-License-Identifier: BSD-3-Clause

import subprocess
from glob import glob

import rclpy
from rclpy.node import Node

from device_msgs.srv import Device


def get_usb_video_devices():
    device_names = []

    for dev in glob("/dev/video*"):
        try:
            out = subprocess.check_output(
                ["udevadm", "info", "--query=property", "--name", dev],
                text=True
            )

            props = {}
            for line in out.splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    props[k] = v

            if props.get("ID_BUS") != "usb":
                continue

            name = (
                props.get("ID_MODEL_FROM_DATABASE")
                or props.get("ID_MODEL")
            )

            if name and name not in device_names:
                device_names.append(name)

        except subprocess.CalledProcessError:
            continue

    return device_names


class DeviceServer(Node):
    def __init__(self):
        super().__init__('device_server')
        self.create_service(Device, 'device', self.handle_device)
        self.get_logger().info('Device service ready.')

    def handle_device(self, request, response):
        self.get_logger().info("handle_device called")
        devices = get_usb_video_devices()

        if not devices:
            response.names = ["no device found"]
        else:
            response.names = devices

        return response


def main():
    rclpy.init()
    node = DeviceServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        

if __name__ == "__main__":
    main()

