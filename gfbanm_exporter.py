"""
    Script for exporting armature animation to gfbanm/tranm format.
"""
import os
import sys
import math

import bpy
from mathutils import Vector, Quaternion
import flatbuffers

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

# pylint: disable=wrong-import-position, import-error

from GFLib.Anim.Animation import AnimationT
from GFLib.Anim.BoneAnimation import BoneAnimationT
from GFLib.Anim.BoneTrack import BoneTrackT
from GFLib.Anim.DynamicRotationTrack import DynamicRotationTrackT
from GFLib.Anim.DynamicVectorTrack import DynamicVectorTrackT
from GFLib.Anim.Info import InfoT
from GFLib.Anim.Vec3 import Vec3T


def export_animation(context: bpy.types.Context, does_loop: bool) -> int | bytearray:
    """
    Exports armature animation to GFBANM/TRANM format.
    :param context: Blender's Context.
    :param does_loop: True if animation is looping.
    :return: GFBANM/TRANM bytearray.
    """
    assert context.object is not None and context.object.type == "ARMATURE",\
        "Target Armature not selected."
    assert context.object.animation_data is not None, "Animation data does not exist."
    assert context.object.animation_data.action is not None,\
        "No Action selected for Animation data."
    animation = AnimationT()
    animation.info = InfoT()
    animation.info.keyFrames = context.scene.frame_end - context.scene.frame_start + 1
    animation.info.frameRate = int(context.scene.render.fps / context.scene.render.fps_base)
    animation.info.doesLoop = int(does_loop)
    animation.skeleton = BoneAnimationT()
    animation.skeleton.tracks = []
    current_frame = context.scene.frame_current
    for pose_bone in context.object.pose.bones:
        print(f"Exporting keyframes for {pose_bone.name} track.")
        transforms = get_track_transforms_from_posebone(context, pose_bone)
        track = BoneTrackT()
        track.name = pose_bone.name
        track.translateType = 2
        track.translate = DynamicVectorTrackT()
        track.translate.co = []
        track.rotateType = 2
        track.rotate = DynamicRotationTrackT()
        track.rotate.co = []
        track.scaleType = 2
        track.scale = DynamicVectorTrackT()
        track.scale.co = []
        for transform in transforms:
            vec = Vec3T()
            vec.x = transform[0][0]
            vec.y = transform[0][1]
            vec.z = transform[0][2]
            track.translate.co.append(vec)
            vec = Vec3T()
            vec.x, vec.y, vec.z = pack_quaternion_to_48bit(transform[1])
            track.rotate.co.append(vec)
            vec = Vec3T()
            vec.x = transform[2][0]
            vec.y = transform[2][1]
            vec.z = transform[2][2]
            track.scale.co.append(vec)
        animation.skeleton.tracks.append(track)
    context.scene.frame_set(current_frame)
    builder = flatbuffers.Builder()
    animation = animation.Pack(builder)
    builder.Finish(animation)
    return builder.Output()

PI_DIVISOR = math.pi / 65536
PI_ADDEND = math.pi / 4.0

def quantize_float(f: float) -> int:
    """
    Packs expanded float into integer.
    :param f: Expanded float.
    :return: Packed integer.
    """
    result = int((f + PI_ADDEND) / PI_DIVISOR)
    return result & 0x7FFF

def pack_quaternion_to_48bit(q: Quaternion) -> (int, int, int):
    """
    Packs Blender Quaternion into 48-bit integer Vector.
    :param q: Blender Quaternion.
    :return: X, Y, Z values of integer Vector.
    """
    q_list = [q.w, q.x, q.y, q.z]
    max_val = max(q_list)
    min_val = min(q_list)
    is_negative = 0
    if abs(min_val) > max_val:
        max_val = min_val
        is_negative = 1
    max_index = q_list.index(max_val)
    if is_negative == 1:
        q_list = [-x for x in q_list]
    if max_index == 0:
        tx = quantize_float(q_list[3])
        ty = quantize_float(q_list[1])
        tz = quantize_float(q_list[2])
    elif max_index == 1:
        tx = quantize_float(q_list[0])
        ty = quantize_float(q_list[3])
        tz = quantize_float(q_list[2])
    elif max_index == 2:
        tx = quantize_float(q_list[0])
        ty = quantize_float(q_list[1])
        tz = quantize_float(q_list[3])
    else:
        tx = quantize_float(q_list[0])
        ty = quantize_float(q_list[1])
        tz = quantize_float(q_list[2])
    pack = (tz << 30) | (ty << 15) | tx
    pack = (pack << 3) | ((is_negative << 2) | max_index)
    return pack & 0xFFFF, (pack >> 16) & 0xFFFF, (pack >> 32) & 0xFFFF


def get_track_transforms_from_posebone(context: bpy.types.Context, pose_bone: bpy.types.PoseBone)\
        -> list[(Vector, Quaternion, Vector)]:
    """
    Returns list of track transforms for every keyframe of animation.
    To-do: The resulting location and rotation are currently incorrect, needs a fix.
    :param context: Blender's Context.
    :param pose_bone: Target PoseBone.
    :return: List of (Location, Rotation, Scaling) track transform tuples.
    """
    transforms = []
    matrix = pose_bone.bone.matrix_local
    if pose_bone.parent:
        matrix = pose_bone.parent.bone.matrix_local.inverted() @ matrix
    loc, rot, _ = matrix.decompose()
    for i in range(context.scene.frame_start, context.scene.frame_end + 1):
        context.scene.frame_set(i)
        pose_loc, pose_rot, _ = pose_bone.matrix.decompose()
        transform_loc = pose_loc - loc
        transform_rot = rot @ pose_rot
        transform_scale = pose_bone.scale
        transforms.append((transform_loc, transform_rot, transform_scale))
    return transforms
