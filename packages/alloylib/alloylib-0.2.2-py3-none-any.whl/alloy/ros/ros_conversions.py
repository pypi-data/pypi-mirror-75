# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
Different functions that convert Ros messages to Numpy array
"""

import numpy as np


from geometry_msgs.msg import(
    Wrench,
    Twist,
    Pose,
    Point
)

__all__ = [
    'numpy_to_wrench', 'wrench_to_numpy', 'twist_to_numpy', 'numpy_to_twist',
    'pose_to_numpy', 'dict_to_pose', 'transform_to_numpy','transform_to_pose',
    'point_to_numpy','numpy_to_point','numpy_to_pose'
]


def dict_to_pose(dict_input):
    """
    Convert a dictionary with the same layout as Pose into a Pose object
    """
    p = Pose()
    if 'position' not in dict_input or 'orientation' not in dict_input:
        raise SyntaxError("position or orientation doesn't exist in dict")
    if 'x' in dict_input["position"]:
        p.position.x = dict_input["position"]["x"]
    if 'y' in dict_input["position"]:
        p.position.y = dict_input["position"]["y"]
    if 'z' in dict_input["position"]:
        p.position.z = dict_input["position"]["z"]
    if 'x' in dict_input["orientation"]:
        p.orientation.x = dict_input["orientation"]["x"]
    if 'y' in dict_input["orientation"]:
        p.orientation.y = dict_input["orientation"]["y"]
    if 'z' in dict_input["orientation"]:
        p.orientation.z = dict_input["orientation"]["z"]
    if 'w' in dict_input["orientation"]:
        p.orientation.w = dict_input["orientation"]["w"]
    return p


def numpy_to_wrench(arr):
    """Convert numpy array into wrench
    """
    msg = Wrench()
    msg.force.x = arr[0]
    msg.force.y = arr[1]
    msg.force.z = arr[2]
    msg.torque.x = arr[3]
    msg.torque.y = arr[4]
    msg.torque.z = arr[5]
    return msg


def wrench_to_numpy(wrench):
    """Convert Geometry_msgs.Wrench to a numpy array
    where [0:3] are the force and [3:] are torque
    """
    arr = np.zeros((6,))
    arr[0] = wrench.force.x
    arr[1] = wrench.force.y
    arr[2] = wrench.force.z
    arr[3] = wrench.torque.x
    arr[4] = wrench.torque.y
    arr[5] = wrench.torque.z
    return arr


def twist_to_numpy(twist):
    """Convert twist to numpy
    """
    arr = np.zeros((6,))
    arr[0] = twist.linear.x
    arr[1] = twist.linear.y
    arr[2] = twist.linear.z
    arr[3] = twist.angular.x
    arr[4] = twist.angular.y
    arr[5] = twist.angular.z
    return arr


def numpy_to_twist(np_arr):
    """Convert a (6,) numpy array to
    twist given linear first, follow by angular
    """
    msg = Twist()
    msg.linear.x = np_arr[0]
    msg.linear.y = np_arr[1]
    msg.linear.z = np_arr[2]
    msg.angular.x = np_arr[3]
    msg.angular.y = np_arr[4]
    msg.angular.z = np_arr[5]
    return msg


def pose_to_numpy(pose):
    """Convert Pose to Numpy array 
    """

    arr = np.zeros((7,))
    arr[0] = pose.position.x
    arr[1] = pose.position.y
    arr[2] = pose.position.z
    arr[3] = pose.orientation.w
    arr[4] = pose.orientation.x
    arr[5] = pose.orientation.y
    arr[6] = pose.orientation.z
    return arr

def numpy_to_pose(pose_np):
    pose = Pose()
    pose.position.x = pose_np[0]
    pose.position.y = pose_np[1]
    pose.position.z = pose_np[2]
    pose.orientation.w = pose_np[3]
    pose.orientation.x = pose_np[4]
    pose.orientation.y = pose_np[5]
    pose.orientation.z = pose_np[6]
    return pose

def point_to_numpy(point) -> np.array:
    """Convert a Geometry_msgs/Point to a (3,) numpy array

    Parameters
    ----------
    point : geometry_msgs.msg.Point
        Point Message       

    Returns
    -------
    np.array
        Numpy array holding the value.
    """
    arr = np.zeros((3,))
    arr[0] = point.x
    arr[1] = point.y
    arr[2] = point.z
    return arr

def numpy_to_point(point_np):
    p = Point()
    p.x = point_np[0]
    p.y = point_np[1]
    p.z = point_np[2]
    return p

def transform_to_numpy(transform):
    """Convert geometry_msgs/Transform to a Numpy array with 
    format [(translation) (rotation[w,x,y,s])]

    Arguments:
        transform {geometry_msgs/Transform} -- Transform message

    Return:
        numpy.array (7,0) describing the position and quaternion
    """

    arr = np.zeros((7,))
    arr[0] = transform.translation.x
    arr[1] = transform.translation.y
    arr[2] = transform.translation.z
    arr[3] = transform.rotation.w
    arr[4] = transform.rotation.x
    arr[5] = transform.rotation.y
    arr[6] = transform.rotation.z
    return arr

def transform_to_pose(transform):

    p = Pose()
    p.position.x = transform.translation.x
    p.position.y = transform.translation.y
    p.position.z = transform.translation.z
    p.orientation.w = transform.rotation.w
    p.orientation.x = transform.rotation.x
    p.orientation.y = transform.rotation.y
    p.orientation.z = transform.rotation.z
    return p