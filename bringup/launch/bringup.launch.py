import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node, PushRosNamespace, SetRemap
from launch.actions import ExecuteProcess, GroupAction
from launch import LaunchDescription, LaunchService
from launch.actions import IncludeLaunchDescription, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def launch_setup(context):

    controller_package_path = get_package_share_directory('controller')
    camera_package_path = get_package_share_directory('orbbec_camera')
    peripherals_package_path = get_package_share_directory('peripherals')
	lidar_package_path = get_package_share_directory('ldlidar_stl_ros2')

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(controller_package_path, 'launch/controller.launch.py')),
    )
    
    # we want to deal with the fact that camera has a nested namespace
    # so we need to manually remap the tf topics from /ROBOTNAME/camera/tf to /ROBOTNAME/tf
    # and from /ROBOTNAME/camera/tf_static /ROBOTNAME/tf_static
    depth_camera_launch = GroupAction(actions=[
    	SetRemap(src='/tf', dst=f'/{os.uname().nodename}/tf'),
    	SetRemap(src='/tf_static', dst=f'/{os.uname().nodename}/tf_static'),
    	IncludeLaunchDescription(
	        PythonLaunchDescriptionSource(
        	    os.path.join(camera_package_path, 'launch/gemini_330_series.launch.py'),
		)
	)
    ])    

    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(lidar_package_path, 'launch/ld19.launch.py')),
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
            ]

def generate_launch_description():
    return LaunchDescription([
        GroupAction(
            actions=[
                PushRosNamespace(os.uname().nodename),
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
