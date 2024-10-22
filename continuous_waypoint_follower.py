#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped

class WaypointFollowerClient(Node):

    def __init__(self):
        super().__init__('waypoint_follower_client')
        self._action_client = ActionClient(self, FollowWaypoints, '/follow_waypoints')

        # Define waypoints directly in the script
        self.waypoints = self.define_waypoints()

        # Track current waypoint index
        self.current_waypoint_index = 0

    def define_waypoints(self):
        # List of (x, y) coordinates for waypoints
        waypoint_coords = [
            (0.01, 0.01),

            (-10.7, -7.8),
            (-14.7, -7.8),
            (-14.7, -5.0),
            (-10.7, -5.0),

            (-10.9, -2.7),
            (-14.8, -2.7),
            (-14.8, -1.5),
            (-10.9, -1.5),

            (-11.2, 4.4),
            (-14.5, 4.4),
            (-14.4, 7.5),
            (-11.2, 7.5),

            (-7.3, 0.24),
            (-3.95, -0.38),
            (-4.1, 3.22),
            (-6.65, 3.4),

            (-0.9, 7.9),
            (18.0, 7.9),
            (-0.9, 7.9),
            (0.45, 3.6),
            (17.5, 3.6),

            (15.35, -0.92),
            (16.83, -2.64),
            (15.35, -4.15),
            (13.42, -2.4),
            (15.18, -0.8),

            (9.2, 1.56),
            (9.5, -4.36),
            (2.23, -4.46),
            (2.5, 1.23),
            (9.04, 1.64),

            (0.01, 0.01)
        ]

        # Convert the waypoints into PoseStamped
        waypoints = []
        for x, y in waypoint_coords:
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation.w = 1.0  # Assuming flat orientation (no rotation)
            waypoints.append(pose)
        
        return waypoints

    def send_goal(self):
        goal_msg = FollowWaypoints.Goal()
        goal_msg.poses = self.waypoints

        # Send the goal and print which waypoint is currently being sent
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return
        self.get_logger().info('Goal accepted :)')

        # After accepting the goal, start tracking which waypoint is being followed
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Goal completed. Result: {}'.format(result))

        # Loop through each waypoint and log the currently followed one
        for idx, waypoint in enumerate(self.waypoints):
            self.get_logger().info(f'Following waypoint {idx + 1}: ({waypoint.pose.position.x}, {waypoint.pose.position.y})')
        
        # Optionally, loop back to the first waypoint or stop after completing all waypoints
        self.get_logger().info('All waypoints completed. Restarting...')
        self.send_goal()  # Restart to follow the waypoints again

def main(args=None):
    rclpy.init(args=args)
    waypoint_follower_client = WaypointFollowerClient()

    input("Press Enter to start continuous waypoint following...")
    
    try:
        waypoint_follower_client.send_goal()  # Start the loop
        rclpy.spin(waypoint_follower_client)
    except KeyboardInterrupt:
        print("Stopping waypoint following loop.")
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
