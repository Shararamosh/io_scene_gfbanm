"""
    Script for importing animation from deserialized gfbanm file.
"""

import os
import sys
import math
import logging

import bpy
from mathutils import Vector, Euler, Quaternion, Matrix
import numpy as np

log = logging.getLogger(__name__)
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from GFLib.Anim.DynamicRotationTrack import DynamicRotationTrackT
from GFLib.Anim.DynamicVectorTrack import DynamicVectorTrackT
from GFLib.Anim.FixedRotationTrack import FixedRotationTrackT
from GFLib.Anim.FixedVectorTrack import FixedVectorTrackT
from GFLib.Anim.Framed16RotationTrack import Framed16RotationTrackT
from GFLib.Anim.Framed16VectorTrack import Framed16VectorTrackT
from GFLib.Anim.Framed8RotationTrack import Framed8RotationTrackT
from GFLib.Anim.Framed8VectorTrack import Framed8VectorTrackT
from GFLib.Anim.Animation import AnimationT
from GFLib.Anim.BoneTrack import BoneTrackT
from GFLib.Anim.Vec3 import Vec3T
from GFLib.Anim.sVec3 import sVec3T


def import_animation(
    context: bpy.types.Context,
    file_path: str,
    euler_rotation_mode: str,
):
    """
    Imports animation from processing gfbanm file.
    :param context: Blender's Context.
    :param file_path: Path to gfbanm file.
    :param euler_rotation_mode: Euler Rotation Mode string.
    :param add_euler_rotation: Additive Euler Rotation.
    """
    if context.object is None or context.object.type != "ARMATURE":
        raise OSError("Target Armature not selected.")
    print("Armature name: " + context.object.name + ".")
    anim_name = os.path.splitext(os.path.basename(file_path))[0]
    print("Animation name: " + anim_name + ".")
    print("Euler Rotation Mode: " + euler_rotation_mode + ".")
    with open(file_path, "rb") as file:
        anm = AnimationT.InitFromPackedBuf(bytearray(file.read()), 0)
        if anm.info is None:
            raise OSError(file_path + " contains invalid info chunk.")
        if anm.info.keyFrames < 1:
            raise OSError(file_path + " contains invalid info.keyFrames chunk.")
        print("Keyframes amount: " + str(anm.info.keyFrames) + ".")
        if anm.info.frameRate < 1:
            raise OSError(file_path + " contains invalid info.frameRate chunk.")
        print("Framerate: " + str(anm.info.frameRate) + " FPS.")
        if anm.skeleton is None:
            raise OSError(file_path + " contains invalid skeleton chunk.")
        if anm.skeleton.tracks is None:
            raise OSError(file_path + " contains invalid skeleton.tracks chunk.")
        if anm.skeleton.initData is not None:
            print(
                "skeleton.initData.isInit: " + str(anm.skeleton.initData.isInit) + "."
            )
            print(
                "skeleton.initData.transform: "
                + str(anm.skeleton.initData.transform)
                + "."
            )
        print("Tracks amount: " + str(len(anm.skeleton.tracks)) + ".")
        previous_mode = context.object.mode
        previous_frame = context.scene.frame_current
        select_bones = {}
        for bone in context.object.data.bones:
            select_bones.update({bone: bone.select})
        if context.object.mode != "POSE":
            bpy.ops.object.mode_set(mode="POSE")
        apply_animation_to_tracks(
            context,
            anim_name,
            anm.info.frameRate,
            anm.info.keyFrames,
            anm.skeleton.tracks,
        )
        for bone, select in select_bones.items():
            bone.select = select
        if previous_frame != context.scene.frame_current:
            context.scene.frame_set(previous_frame)
        if previous_mode != context.object.mode:
            bpy.ops.object.mode_set(mode=previous_mode)


def apply_animation_to_tracks(
    context: bpy.types.Context,
    anim_name: str,
    frame_rate: int,
    key_frames: int,
    tracks: list[BoneTrackT | None],
):
    """
    Applies animation to bones of selected Armature.
    :param context: Blender's Context.
    :param anim_name: Action name.
    :param frame_rate: Framerate.
    :param key_frames: Keyframes amount.
    :param tracks: List of BoneTrack objects.
    :param euler_rotation_mode: Euler Rotation Mode string.
    :param add_euler_rotation: Additive Euler Rotation.
    """
    assert (
        context.object is not None and context.object.type == "ARMATURE"
    ), "Selected object is not Armature."

    action = None

    for track in tracks:

        if track is None or track.name is None or track.name == "":
            continue

        print("Creating keyframes for " + track.name + " track.")

        if track.name not in context.object.pose.bones.keys():
            continue

        pose_bone = context.object.pose.bones[track.name]

        t_list = get_vector_track_transforms(track.translate, key_frames)
        s_list = get_vector_track_transforms(track.scale, key_frames)
        r_list = get_rotation_track_transforms(track.rotate, key_frames)

        if context.object.animation_data is None:
            context.object.animation_data_create()

        if action is None:
            action = bpy.data.actions.new(anim_name)
            action.use_fake_user = True
            context.object.animation_data.action = action
            context.scene.render.fps = frame_rate
            context.scene.render.fps_base = 1.0

        apply_track_transforms_to_posebone(
            context, pose_bone, list(zip(t_list, r_list, s_list))
        )

    context.scene.frame_end = context.scene.frame_start + key_frames - 1


def apply_track_transforms_to_posebone(
    context: bpy.types.Context,
    pose_bone: bpy.types.PoseBone,
    transforms: list[(Vector | None, Quaternion | None, Vector | None)],
):
    """
    Applies global transforms to PoseBone for every keyframe of animation.
    :param context: Blender's Context.
    :param pose_bone: Target PoseBone.
    :param transforms: List of (Location, Rotation, Scaling) global transform tuples.
    :param print_first_frame_transforms_info: Print information about applied first frame transforms or not.
    """

    matrix = pose_bone.bone.matrix_local

    if pose_bone.parent:    
        matrix = pose_bone.parent.bone.matrix_local.inverted() @ matrix
    
    loc, rot, scale = matrix.decompose()

    for i, transform in enumerate(transforms):
        pose_bone.location = transform[0] - loc
        pose_bone.rotation_quaternion = rot.conjugated() @ transform[1]
        pose_bone.scale = Vector((transform[2].x / scale.x, transform[2].y / scale.y, transform[2].z / scale.z))
        pose_bone.keyframe_insert(data_path="location", frame=i)
        pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=i)
        pose_bone.keyframe_insert(data_path="scale", frame=i)


def get_posebone_global_matrix(pose_bone: bpy.types.PoseBone) -> Matrix:
    """
    Returns global transform Matrix of PoseBone.
    :param pose_bone: PoseBone.
    :return: Global transform Matrix.
    """
    assert (
        pose_bone is not None
    ), "Can't get global transform Matrix for None pose bone."
    return pose_bone.id_data.matrix_world @ pose_bone.matrix


def set_posebone_global_matrix(pose_bone: bpy.types.PoseBone, m: Matrix):
    """
    Applies global transform Matrix to PoseBone.
    :param pose_bone: PoseBone.
    :param m: Global transform Matrix.
    """
    assert (
        pose_bone is not None
    ), "Can't set global transform Matrix for None pose bone."
    pose_bone.matrix = pose_bone.id_data.matrix_world.inverted() @ m


def get_vector_track_transforms(
    track: (
        DynamicVectorTrackT
        | FixedVectorTrackT
        | Framed16VectorTrackT
        | Framed8VectorTrackT
        | None
    ),
    key_frames: int,
) -> list[Vector | None]:
    """
    Returns list with transforms from VectorTrack object.
    :param track: VectorTrack object.
    :param key_frames: Amount of keyframes in animation.
    :return: List of Vectors or None.
    """

    assert key_frames > 0, "Keyframes amount is less than 1."
    transforms: list[Vector | None] = [None] * key_frames

    if track is None or track.co is None:
        return transforms

    if isinstance(track, FixedVectorTrackT):
        v = Vector((track.co.x, track.co.y, track.co.z))
        transforms = [v] * key_frames

    elif isinstance(track, DynamicVectorTrackT):
        for i in range(min(len(track.co), key_frames)):
            transforms[i] = Vector((track.co[i].x, track.co[i].y, track.co[i].z))

    elif isinstance(track, Framed16VectorTrackT) or isinstance(track, Framed8VectorTrackT):
        frameDataX = np.array([track.co[i].x for i in range(len(track.co))])
        frameDataY = np.array([track.co[i].y for i in range(len(track.co))])
        frameDataZ = np.array([track.co[i].z for i in range(len(track.co))])
        iframeDataX = np.interp(np.arange(key_frames), np.array(track.frames), frameDataX)
        iframeDataY = np.interp(np.arange(key_frames), np.array(track.frames), frameDataY)
        iframeDataZ = np.interp(np.arange(key_frames), np.array(track.frames), frameDataZ)
        for frame, (x, y, z) in enumerate(zip(iframeDataX, iframeDataY, iframeDataZ)):
                transforms[frame] = Vector((x, y, z))
    return transforms


def get_rotation_track_transforms(
    track: (
        DynamicRotationTrackT
        | FixedRotationTrackT
        | Framed16RotationTrackT
        | Framed8RotationTrackT
        | None
    ),
    key_frames: int,
) -> list[Quaternion | None]:
    """
    Returns list with transforms from RotationTrack object.
    :param track: RotationTrack object.
    :param key_frames: Amount of keyframes in animation.
    :return: List of Eulers or None.
    """
    assert key_frames > 0, "Keyframes amount is less than 1."
    transforms: list[Quaternion | None] = [None] * key_frames
    if isinstance(track, FixedRotationTrackT):
        e = get_quaternion_from_packed(track.co, 0)
        transforms = [e] * key_frames
    elif isinstance(track, DynamicRotationTrackT):
        for i in range(min(len(track.co), key_frames)):
            transforms[i] = get_quaternion_from_packed(track.co[i], i)
    elif isinstance(track, Framed16RotationTrackT) or isinstance(track, Framed8RotationTrackT):
        frameData = np.array([get_quaternion_from_packed(track.co[i], i) for i in range(len(track.co))])
        interpolatedFrames = np.array([np.interp(np.arange(key_frames), np.array(track.frames), data) for data in frameData.transpose()]).T
        for frame, quat in enumerate(interpolatedFrames):
            transforms[frame] = Quaternion(quat)

    return transforms


SCALE = 0x7FFF
PI_QUARTER = math.pi / 4.0
PI_HALF = math.pi / 2.0


def expand_float(i: int) -> float:
    return i * (PI_HALF / SCALE) - PI_QUARTER


def unpack48bitQuaternion(x: int, y: int, z: int) -> Quaternion:
    pack = (z << 32) | (y << 16) | x

    q1 = expand_float((pack >> 3) & 0x7FFF)
    q2 = expand_float((pack >> 18) & 0x7FFF)
    q3 = expand_float((pack >> 33) & 0x7FFF)

    values = [q1, q2, q3]

    max_component = max(1.0 - (q1 * q1 + q2 * q2 + q3 * q3), 0.0)
    max_component = math.sqrt(max_component)

    missing_component = pack & 0b0011

    values.insert(missing_component, max_component)

    is_negative = (pack & 0b0100) != 0

    return (
        Quaternion((values[3], values[0], values[1], values[2]))
        if not is_negative
        else Quaternion((-values[3], -values[0], -values[1], -values[2]))
    )


def get_quaternion_from_packed(
    vec: Vec3T | sVec3T | None, key_frame
) -> Quaternion | None:
    """
    Converts packed quaternion components into a Quaternion object.
    :param vec: Packed Vector object.
    :return: Quaternion object.
    """
    if vec is None:
        return None
    quat = unpack48bitQuaternion(vec.x, vec.y, vec.z)
    return quat
