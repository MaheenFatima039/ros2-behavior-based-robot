from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_share = get_package_share_directory('my_diffbot')
    world_file = os.path.join(pkg_share, 'worlds', 'follow_world.sdf')
    urdf_file = os.path.join(pkg_share, 'urdf', 'diffbot.urdf')

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': open(urdf_file).read()
        }]
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_diffbot',
            '-topic', 'robot_description'
        ],
        output='screen'
    )

    perception = Node(
        package='my_diffbot',
        executable='perception_node',
        output='screen'
    )

    control = Node(
        package='my_diffbot',
        executable='follow_stop_node',
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        perception,
        control
    ])

