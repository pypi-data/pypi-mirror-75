#  -*- coding: utf-8 -*-

"""A class for straightforward tracking with an ARuCo
"""
from time import time
from numpy import nditer, array, mean, float32, loadtxt
from numpy import min as npmin
from numpy import max as npmax
from numpy.linalg import norm
import cv2.aruco as aruco # pylint: disable=import-error
from cv2 import VideoCapture, imshow
import cv2

from sksurgerycore.transforms.matrix import (construct_rotm_from_euler,
                                             construct_rigid_transformation,
                                             )

from sksurgerycore.baseclasses.tracker import SKSBaseTracker

def _get_poses_without_calibration(marker_corners):
    """
    Returns a tracking data for and uncalibrated camera.
    x and y are the screen pixel coordinates.
    z is based on the size of the tag in pixels, there is no
    rotation
    """
    tracking = []
    for marker in marker_corners:
        means = mean(marker[0], axis=0)
        maxs = npmax(marker[0], axis=0)
        mins = npmin(marker[0], axis=0)
        size = norm(maxs - mins)
        tracking.append(array([[1.0, 0.0, 0.0, means[0]],
                               [0.0, 1.0, 0.0, means[1]],
                               [0.0, 0.0, 1.0, -size],
                               [0.0, 0.0, 0.0, 1.0]], dtype=float32))
    return tracking


def _load_calibration(textfile):
    """
    loads a calibration from a text file
    """
    projection_matrix = loadtxt(textfile, dtype=float32, max_rows=3)
    distortion = loadtxt(textfile, dtype=float32, skiprows=3, max_rows=1)

    return projection_matrix, distortion

class ArUcoTracker(SKSBaseTracker):
    """
    Base class for communication with trackers.
    Ideally all surgery tracker classes will implement
    this interface
    """
    def __init__(self, configuration):
        """
        Initialises and Configures the ArUco detector

        :param configuration: A dictionary containing details of the tracker.

            video source: defaults to 0

            aruco dictionary: defaults to DICT_4X4_50

            marker size: defaults to 50 mm

            camera projection matrix: defaults to None

            camera distortion: defaults to None

        :raise Exception: ImportError, ValueError
        """

        self._ar_dict = None
        self._camera_projection_matrix = None
        self._camera_distortion = array([0.0, 0.0, 0.0, 0.0, 0.0],
                                        dtype=float32)
        self._use_camera_projection = False
        self._state = None

        self._frame_number = 0

        self._debug = configuration.get("debug", False)

        video_source = configuration.get("video source", 0)

        if video_source != 'none':
            self._capture = VideoCapture()
        else:
            self._capture = None

        ar_dictionary_name = getattr(aruco, 'DICT_4X4_50')
        if "aruco dictionary" in configuration:
            dictionary_name = configuration.get("aruco dictionary")
            try:
                ar_dictionary_name = getattr(aruco, dictionary_name)
            except AttributeError:
                raise ImportError(('Failed when trying to import {} from cv2.'
                                   'aruco. Check dictionary exists.')
                                  .format(dictionary_name))

        self._ar_dict = aruco.getPredefinedDictionary(ar_dictionary_name)

        self._marker_size = configuration.get("marker size", 50)

        if "calibration" in configuration:
            self._camera_projection_matrix, self._camera_distortion = \
                _load_calibration(configuration.get("calibration"))
            self._check_pose_estimation_ok()

        if video_source != 'none':
            if self._capture.open(video_source):
                #try setting some properties
                if "capture properties" in configuration:
                    props = configuration.get("capture properties")
                    for prop in props:
                        cvprop = getattr(cv2, prop)
                        value = props[prop]
                        self._capture.set(cvprop, value)

                self._state = "ready"
            else:
                raise OSError('Failed to open video source {}'
                              .format(video_source))
        else:
            self._state = "ready"


    def _check_pose_estimation_ok(self):
        """Checks that the camera projection matrix and camera distortion
        matrices can be used to estimate pose"""
        if (self._camera_projection_matrix.shape == (3, 3) and
                self._camera_projection_matrix.dtype == float32):
            self._use_camera_projection = True
        else:
            raise ValueError(('Camera projection matrix needs to be 3x3 and'
                              'float32'), self._camera_projection_matrix.shape,
                             self._camera_projection_matrix.dtype)

    def close(self):
        """
        Closes the connection to the Tracker and
        deletes the tracker device.

        :raise Exception: ValueError
        """
        if self._capture is not None:
            self._capture.release()
            del self._capture
        self._state = None

    def get_frame(self, frame=None):
        """Gets a frame of tracking data from the Tracker device.

        :params frame: an image to process, if None, we use the OpenCV
            video source.
        :return:
            port_numbers : list of port handles, one per tool

            time_stamps : list of timestamps (cpu clock), one per tool

            frame_numbers : list of framenumbers (tracker clock) one per tool

            tracking : list of 4x4 tracking matrices, rotation and position,
            or if use_quaternions is true, a list of tracking quaternions,
            column 0-2 is x,y,z column 3-6 is the rotation as a quaternion.

            tracking_quality : list the tracking quality, one per tool.

        :raise Exception: ValueError
        """
        if self._state != "tracking":
            raise ValueError('Attempted to get frame, when not tracking')

        if self._capture is not None:
            _, frame = self._capture.read()

        if frame is None:
            raise ValueError('Frame not set, and capture.read failed')

        marker_corners, marker_ids, _ = \
                aruco.detectMarkers(frame, self._ar_dict)

        port_handles = []
        time_stamps = []
        frame_numbers = []
        tracking_quality = []
        tracking = None

        timestamp = time()

        if marker_corners:
            for marker in nditer(marker_ids):
                port_handles.append(marker.item())
                time_stamps.append(timestamp)
                frame_numbers.append(self._frame_number)
                tracking_quality.append(1.0)

            if self._use_camera_projection:
                tracking = self._get_poses_with_calibration(marker_corners)
            else:
                tracking = _get_poses_without_calibration(marker_corners)

            if self._debug:
                aruco.drawDetectedMarkers(frame, marker_corners)

        self._frame_number += 1
        if self._debug:
            imshow('frame', frame)

        return (port_handles, time_stamps, frame_numbers, tracking,
                tracking_quality)

    def _get_poses_with_calibration(self, marker_corners):
        rvecs, tvecs, _ = \
            aruco.estimatePoseSingleMarkers(marker_corners,
                                            self._marker_size,
                                            self._camera_projection_matrix,
                                            self._camera_distortion)
        tracking = []
        t_index = 0
        for rvec in rvecs:
            rot_mat = construct_rotm_from_euler(rvec[0][0], rvec[0][1],
                                                rvec[0][2], 'xyz',
                                                is_in_radians=True)
            tracking.append(construct_rigid_transformation(rot_mat,
                                                           tvecs[t_index][0]))
            t_index += 1
        return tracking

    def get_tool_descriptions(self):
        """ Returns tool descriptions """
        return self._capture

    def start_tracking(self):
        """
        Tells the tracking device to start tracking.
        :raise Exception: ValueError
        """
        if self._state == "ready":
            self._state = "tracking"
        else:
            raise ValueError('Attempted to start tracking, when not ready')

    def stop_tracking(self):
        """
        Tells the tracking devices to stop tracking.
        :raise Exception: ValueError
        """
        if self._state == "tracking":
            self._state = "ready"
        else:
            raise ValueError('Attempted to stop tracking, when not tracking')
