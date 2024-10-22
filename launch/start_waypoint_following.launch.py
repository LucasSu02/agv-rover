import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'agv-rover'  # Ensure your package name is correct

    # Waypoint follower node
    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[{'use_sim_time': True}, {'waypoints': '/home/fawzan/Documents/agv_rover/src/agv-rover/waypoints/waypoints.yaml'}]  # Ensure this points to your waypoints file
    )

    return LaunchDescription([
        waypoint_follower  # Add waypoint follower here
    ])
