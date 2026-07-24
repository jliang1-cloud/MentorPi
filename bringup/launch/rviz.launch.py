from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
            namespace=os.uname().nodename
        )
    ])
