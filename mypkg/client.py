#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from device_msgs.srv import Device

class DeviceClient(Node):
    def __init__(self):
        super().__init__('device_client')
        self.client = self.create_client(Device, 'device')
        self.timer = self.create_timer(1.0, self.try_call)
        self.finished = False

    def try_call(self):
        if not self.client.service_is_ready():
            self.get_logger().info('Waiting for service...')
            return

        self.timer.cancel()
        req = Device.Request()
        self.future = self.client.call_async(req)
        self.future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'devices: {response.names}')
        except Exception as e:
            self.get_logger().error(str(e))
        finally:
            self.finished = True
            self.destroy_node()


def main():
    rclpy.init()
    node = DeviceClient()
    try:
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        node.destroy_node()
    finally:
        pass

if __name__ == "__main__":
    main()