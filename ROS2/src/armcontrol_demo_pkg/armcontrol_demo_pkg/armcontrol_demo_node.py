import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from sensor_msgs.msg import JointState


class ArmControlDemo(Node):
    """Simple demo node that publishes joint states with runtime-adjustable angles."""

    def __init__(self):
        super().__init__('armcontrol_demo')

        self.publisher = self.create_publisher(JointState, 'joint_states', 10)

        # Declare parameters for each joint angle
        for i in range(1, 7):
            self.declare_parameter(f'joint{i}_angle', 0.0)

        self.msg = JointState()
        self.msg.name = [f'joint{i}' for i in range(1, 7)]
        self.update_from_parameters()

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def update_from_parameters(self):
        self.msg.position = [self.get_parameter(f'joint{i}_angle').value for i in range(1, 7)]

    def parameter_callback(self, params):
        for param in params:
            if param.name.startswith('joint') and param.name.endswith('_angle'):
                try:
                    index = int(param.name[5]) - 1
                    if 0 <= index < 6:
                        self.msg.position[index] = param.value
                except ValueError:
                    pass
        return SetParametersResult(successful=True)

    def timer_callback(self):
        self.msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)
    node = ArmControlDemo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

