import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node, PushRosNamespace
from launch.actions import ExecuteProcess, GroupAction
from launch import LaunchDescription, LaunchService
from launch.actions import IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def launch_setup(context):
    compiled = 'True'
    if compiled == 'True':
        controller_package_path = get_package_share_directory('controller')
        camera_package_path = get_package_share_directory('orbbec_camera')
        peripherals_package_path = get_package_share_directory('peripherals')
    else:
        controller_package_path = '/home/jeffreyliang/robot_ws/src/driver/controller'
        app_package_path = '/home/jeffreyliang/robot_ws/src/app'
        peripherals_package_path = '/home/jeffreyliang/robot_ws/src/peripherals'

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(controller_package_path, 'launch/controller.launch.py')),
    )
    
    depth_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(camera_package_path, 'launch/gemini_330_series.launch.py')),
    )
    camera_transform_run = LaunchDescription([
        Node(
            package='astra_plus_transform',
            executable='camera_transform_node'
        )
    ])

    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(peripherals_package_path, 'launch/lidar.launch.py')),
    )

    init_pose_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(controller_package_path, 'launch/init_pose.launch.py')),
        launch_arguments={
            'namespace': '',  
            'use_namespace': 'false',
            'action_name': 'init',
        }.items(),
    )

    joystick_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(peripherals_package_path, 'launch/joystick_control.launch.py')),
    )

    return [
            controller_launch,
            depth_camera_launch,
            lidar_launch,
            joystick_control_launch,
            init_pose_launch,
            camera_transform_run
            ]

def generate_launch_description():
    return LaunchDescription([
        GroupAction(
            actions=[
                PushRosNamespace('magtail'),
                OpaqueFunction(function = launch_setup)
            ]
        )
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
