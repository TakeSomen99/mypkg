import rclpy
from rclpy.node import Node
from device_msgs.srv import Device
import subprocess


def get_device_names_cb(request, response):
    devices = []
    try:
        result = subprocess.run(
                ['udevadm', 'info', '--query=all', '--name=/dev/bus/usb'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
        )
        ilnes = result.stdout.splitlines()

        for line in lines:
            if "ATTR{name}" in line:
                name = line.split('=')[1].strip()
                if name not in devices:
                    devices.append(name)
            if len(devices) >= 4:
                break

        response.names = devices
    except Exception as e:
        print(f"Failed to get device name: {e}")
        response.name = []

    return response


def main():
    rclpy.init()
    node = Node("device_service_node")

    srv = node.create_service(Device, "get_device_names", get_device_names_cb)
    node.get_logger().info("DeviceService ready. Wating...")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
