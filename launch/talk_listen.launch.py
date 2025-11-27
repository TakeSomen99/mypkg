import launch
import launch.actions
import launch.substitutions
import lauch_ros.actions

def generate_launch_description():

    talker = lauch_ros.actions.Node(
            package='mypak'
            )
