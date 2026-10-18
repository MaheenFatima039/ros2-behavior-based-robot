import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32
import math

class PerceptionNode(Node):
    """
    Subscribes: /scan
    Publishes:
      /target_distance (Float32)
      /target_detected (Bool)
      /safe_to_move (Bool)
    """
    def __init__(self):
        super().__init__('perception_node')

        self.declare_parameter('front_sector_deg', 30.0)   # +/- degrees
        self.declare_parameter('detect_max_m', 5.0)
        self.declare_parameter('safety_stop_m', 0.8)
        self.declare_parameter('min_valid_m', 0.12)

        self.front_sector_deg = float(self.get_parameter('front_sector_deg').value)
        self.detect_max_m = float(self.get_parameter('detect_max_m').value)
        self.safety_stop_m = float(self.get_parameter('safety_stop_m').value)
        self.min_valid_m = float(self.get_parameter('min_valid_m').value)

        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)
        self.pub_dist = self.create_publisher(Float32, '/target_distance', 10)
        self.pub_det = self.create_publisher(Bool, '/target_detected', 10)
        self.pub_safe = self.create_publisher(Bool, '/safe_to_move', 10)

    def scan_cb(self, msg: LaserScan):
        # Compute indices for front sector around 0 rad
        # angle_min + i*angle_increment = angle
        half = math.radians(self.front_sector_deg)
        if msg.angle_increment == 0.0:
            return

        def angle_to_index(a):
            return int(round((a - msg.angle_min) / msg.angle_increment))

        i0 = max(0, min(len(msg.ranges) - 1, angle_to_index(-half)))
        i1 = max(0, min(len(msg.ranges) - 1, angle_to_index(+half)))
        if i0 > i1:
            i0, i1 = i1, i0

        best = float('inf')
        for r in msg.ranges[i0:i1+1]:
            if not math.isfinite(r):
                continue
            if r < self.min_valid_m:
                continue
            if r < best:
                best = r

        detected = (best < self.detect_max_m)
        safe = (best > self.safety_stop_m) if math.isfinite(best) else False

        if not math.isfinite(best):
            best = 999.0  # for plotting/logging, means "no target"

        self.pub_dist.publish(Float32(data=float(best)))
        self.pub_det.publish(Bool(data=bool(detected)))
        self.pub_safe.publish(Bool(data=bool(safe)))

def main():
    rclpy.init()
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
