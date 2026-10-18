import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Float32

class FollowStopNode(Node):
    """
    Subscribes:
      /target_distance, /target_detected, /safe_to_move
    Publishes:
      /cmd_vel
    States:
      SEARCH -> FOLLOW -> STOP
    """
    def __init__(self):
        super().__init__('follow_stop_node')

        # Parameters
        self.declare_parameter('search_angular_z', 0.5)
        self.declare_parameter('max_linear_x', 0.6)
        self.declare_parameter('kp_linear', 0.4)          # proportional gain
        self.declare_parameter('follow_desired_m', 1.2)   # try to keep this distance

        self.search_angular_z = float(self.get_parameter('search_angular_z').value)
        self.max_linear_x = float(self.get_parameter('max_linear_x').value)
        self.kp_linear = float(self.get_parameter('kp_linear').value)
        self.follow_desired_m = float(self.get_parameter('follow_desired_m').value)

        self.distance = 999.0
        self.detected = False
        self.safe = False
        self.state = "SEARCH"

        self.create_subscription(Float32, '/target_distance', self.dist_cb, 10)
        self.create_subscription(Bool, '/target_detected', self.det_cb, 10)
        self.create_subscription(Bool, '/safe_to_move', self.safe_cb, 10)

        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.loop)

    def dist_cb(self, msg): self.distance = float(msg.data)
    def det_cb(self, msg): self.detected = bool(msg.data)
    def safe_cb(self, msg): self.safe = bool(msg.data)

    def loop(self):
        cmd = Twist()

        if not self.detected:
            self.state = "SEARCH"
            cmd.angular.z = self.search_angular_z
            cmd.linear.x = 0.0

        elif self.detected and not self.safe:
            self.state = "STOP"
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        else:
            self.state = "FOLLOW"
            # Proportional controller to keep distance ~ follow_desired_m
            error = (self.distance - self.follow_desired_m)
            v = self.kp_linear * error
            if v < 0.0:
                v = 0.0
            if v > self.max_linear_x:
                v = self.max_linear_x
            cmd.linear.x = v
            cmd.angular.z = 0.0

        self.get_logger().info(f"STATE={self.state} dist={self.distance:.2f} detected={self.detected} safe={self.safe}")
        self.pub_cmd.publish(cmd)

def main():

    rclpy.init()
    node = FollowStopNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
