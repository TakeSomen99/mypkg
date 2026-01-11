#!/usr/bin/env python3
#SPDX-FileCopyrightText: 2025 TakeSomen99
#SPDX-License-Identifier: BSD-3-Clause

import subprocess
from glob import glob

import rclpy
from rclpy.node import Node

from device_msgs.srv import Device


def get_usb_video_devices():
    """
    外部USB接続の video デバイスのみを列挙し、
    人間が読める製品名を返す
    """
    device_names = []

    for dev in glob("/dev/video*"):
        try:
            # udev からデバイス情報取得
            out = subprocess.check_output(
                ["udevadm", "info", "--query=property", "--name", dev],
                text=True
            )

            props = {}
            for line in out.splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    props[k] = v

            # USB 接続デバイスのみ
            if props.get("ID_BUS") != "usb":
                continue

            # 人間向けの製品名を優先
            name = (
                props.get("ID_MODEL_FROM_DATABASE")
                or props.get("ID_MODEL")
            )

            if name and name not in device_names:
                device_names.append(name)

        except subprocess.CalledProcessError:
            continue

    return device_names


class DeviceService(Node):

    def __init__(self):
        super().__init__("device_service_node")
        self.srv = self.create_service(
            Device,
            "get_device_names",
            self.get_device_names_cb
        )
        self.get_logger().info("DeviceService ready. Waiting...")

    def get_device_names_cb(self, request, response):
        try:
            response.names = get_usb_video_devices()
        except Exception as e:
            self.get_logger().error(f"Failed to get device names: {e}")
            response.names = []

        return response


def main():
    rclpy.init()
    node = DeviceService()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

