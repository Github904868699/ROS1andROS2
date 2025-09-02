import rclpy
from rclpy.node import Node
import json
import serial
import time
from sensor_msgs.msg import JointState

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('arm_robot_driver')
        #self.serial_port = serial.Serial("/dev/ttyACM0", 115200)
        self.serial_port = serial.Serial("/dev/ttyUSB0", 115200)
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)

    @staticmethod
    def calculate_position(rad_input, direc_input, multi_input):
        if rad_input == 0:
            return 2047
        else:
            get_pos = int(2047 + (direc_input * rad_input / 3.1415926 * 2048 * multi_input) + 0.5)
            return get_pos

    def listener_callback(self, msg):
        num_s = 0.2
        num_a = 1
        deg2ang = 57.2957795
        data = json.dumps({'T': 10004, '1':msg.position[0], '2': -msg.position[2], '3': msg.position[1], '4': msg.position[3], '5': msg.position[4], '6': msg.position[5], 'S': num_s, 'A': num_a}) + "\n"
        # data = json.dumps({'T': 10004, '1':msg.position[0], '2': -msg.position[1], '3': msg.position[2], '4': msg.position[3], '5': msg.position[4], '6': msg.position[5], 'S': num_s, 'A': num_a}) + "\n"
        # data = json.dumps({'T': 10003, '1':msg.position[0]*deg2ang, '2': msg.position[1]*deg2ang, '3': -msg.position[2]*deg2ang, '4': msg.position[3]*deg2ang, '5': msg.position[4]*deg2ang, '6': msg.position[5]*deg2ang, 'S': num_s, 'A': num_a}) + "\n"
        #data = json.dumps({'T': 10004, '1': 0, '2':0, '3': 0, '4': 0, '5': 0, '6': 0, 'S': num_s, 'A': num_a}) + "\n"
        try:
            self.serial_port.write(data.encode())
            
            time.sleep(0.02)
            self.get_logger().info(data)
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    
    minimal_subscriber.destroy_node()
    minimal_subscriber.serial_port.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

