import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import UnlessCondition
from launch.substitutions import LaunchConfiguration, Command, TextSubstitution
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    share_dir = get_package_share_directory('pika_remote_piper')

    declared_arguments = [
        DeclareLaunchArgument('paramsFile', default_value=os.path.join(share_dir, 'config', 'piper_rand_params.yaml')),
        # sim:=true no arranca el driver CAN; el brazo lo pone pika_sim (sim_piper_single.launch.py)
        DeclareLaunchArgument('sim', default_value='false'),
        # index_name:=_l o _r: usa los topics de un Sense del montaje doble (start_multi_sensor.bash),
        # p. ej. para teleoperar el Piper simulado con uno de los dos Sense conectados
        DeclareLaunchArgument('index_name', default_value=''),
    ]
    parameter_file = LaunchConfiguration('paramsFile')
    index_name = LaunchConfiguration('index_name')

    locator_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('piper'), 'launch', 'start_single_piper.launch.py')]),
        condition=UnlessCondition(LaunchConfiguration('sim'))
    )

    return LaunchDescription(declared_arguments+[
        locator_launch,
        Node(
            package='pika_remote_piper',
            executable='piper_FK.py',
            name=['piper_FK', index_name],
            parameters=[{'index_name': index_name,
                         'paramsFile': parameter_file}],
            respawn=True,
            output='screen'
        ),
        Node(
            package='pika_remote_piper',
            executable='piper_IK.py',
            name=['piper_IK', index_name],
            parameters=[{'index_name': index_name,
                         'paramsFile': parameter_file}],
            respawn=True,
            output='screen'
        ),
        Node(
            package='pika_remote_piper',
            executable='teleop_piper_publish.py',
            name=['teleop_piper', index_name],
            parameters=[{'index_name': index_name}],
            respawn=True,
            output='screen'
        ),
    ])
