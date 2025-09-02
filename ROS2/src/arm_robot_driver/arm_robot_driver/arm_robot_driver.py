import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
import json
import serial
import time
from sensor_msgs.msg import JointState

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('arm_robot_driver')
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('speed', 0.2)
        self.declare_parameter('acceleration', 1.0)

        serial_port_name = self.get_parameter('serial_port').get_parameter_value().string_value
        try:
            self.serial_port = serial.Serial(serial_port_name, 115200)
        except serial.SerialException as e:
            self.get_logger().warning(f"Unable to open serial port {serial_port_name}: {e}")
            self.serial_port = None

        self.speed = self.get_parameter('speed').value
        self.acceleration = self.get_parameter('acceleration').value

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)

        self.add_on_set_parameters_callback(self.parameter_callback)

    @staticmethod
    def calculate_position(rad_input, direc_input, multi_input):
        if rad_input == 0:
            return 2047
        else:
            get_pos = int(2047 + (direc_input * rad_input / 3.1415926 * 2048 * multi_input) + 0.5)
            return get_pos

    def listener_callback(self, msg):
        deg2ang = 57.2957795
        data = json.dumps({'T': 10004, '1':msg.position[0], '2': -msg.position[2], '3': msg.position[1], '4': msg.position[3], '5': msg.position[4], '6': msg.position[5], 'S': self.speed, 'A': self.acceleration}) + "\n"
        # data = json.dumps({'T': 10004, '1':msg.position[0], '2': -msg.position[1], '3': msg.position[2], '4': msg.position[3], '5': msg.position[4], '6': msg.position[5], 'S': num_s, 'A': num_a}) + "\n"
        # data = json.dumps({'T': 10003, '1':msg.position[0]*deg2ang, '2': msg.position[1]*deg2ang, '3': -msg.position[2]*deg2ang, '4': msg.position[3]*deg2ang, '5': msg.position[4]*deg2ang, '6': msg.position[5]*deg2ang, 'S': num_s, 'A': num_a}) + "\n"
        #data = json.dumps({'T': 10004, '1': 0, '2':0, '3': 0, '4': 0, '5': 0, '6': 0, 'S': num_s, 'A': num_a}) + "\n"
        if self.serial_port:
            try:
                self.serial_port.write(data.encode())
                time.sleep(0.02)
                self.get_logger().info(data)
            except serial.SerialException as e:
                self.get_logger().error(f"Serial write error: {e}")
        else:
            self.get_logger().debug(f"Serial port not available. Data: {data.strip()}")

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'speed':
                self.speed = param.value
            elif param.name == 'acceleration':
                self.acceleration = param.value
            elif param.name == 'serial_port':
                try:
                    if self.serial_port:
                        self.serial_port.close()
                    self.serial_port = serial.Serial(param.value, 115200)
                except serial.SerialException as e:
                    self.get_logger().error(f"Failed to set serial port {param.value}: {e}")
                    return SetParametersResult(successful=False)
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    
    minimal_subscriber.destroy_node()
    minimal_subscriber.serial_port.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

