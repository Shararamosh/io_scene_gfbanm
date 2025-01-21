"""
    Script for exporting armature animation to gfbanm/tranm format.
"""
import os
import sys

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

def pack_quaternion_to_48bit(_q: Quaternion) -> (int, int, int):
    """
    Packs Blender Quaternion into 48-bit integer Vector.
    To-do: Figure out how to actually pack Quaternion to 3x16 bits integers. Returns dummy for now.
    :param _q: Blender Quaternion.
    :return: X, Y, Z values of integer Vector.
    """
    return 0, 0, 0


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
