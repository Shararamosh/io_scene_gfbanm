# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy

from GFLib.Anim.BoneAnimation import BoneAnimation, BoneAnimationT
from GFLib.Anim.CommandAnimation import CommandAnimation, CommandAnimationT
from GFLib.Anim.Info import InfoT, Info
from GFLib.Anim.MaterialAnimation import MaterialAnimation, MaterialAnimationT
from GFLib.Anim.SkinAnimation import SkinAnimation, SkinAnimationT

np = import_numpy()

class Animation(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Animation()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsAnimation(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Animation
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Animation
    def Info(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            obj = Info()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Animation
    def Skeleton(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            obj = BoneAnimation()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Animation
    def Material(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            obj = MaterialAnimation()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Animation
    def Visibility(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            obj = SkinAnimation()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Animation
    def EventData(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            obj = CommandAnimation()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

def AnimationStart(builder):
    builder.StartObject(5)

def Start(builder):
    AnimationStart(builder)

def AnimationAddInfo(builder, info):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(info), 0)

def AddInfo(builder, info):
    AnimationAddInfo(builder, info)

def AnimationAddSkeleton(builder, skeleton):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(skeleton), 0)

def AddSkeleton(builder, skeleton):
    AnimationAddSkeleton(builder, skeleton)

def AnimationAddMaterial(builder, material):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(material), 0)

def AddMaterial(builder, material):
    AnimationAddMaterial(builder, material)

def AnimationAddVisibility(builder, visibility):
    builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(visibility), 0)

def AddVisibility(builder, visibility):
    AnimationAddVisibility(builder, visibility)

def AnimationAddEventData(builder, eventData):
    builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(eventData), 0)

def AddEventData(builder, eventData):
    AnimationAddEventData(builder, eventData)

def AnimationEnd(builder):
    return builder.EndObject()

def End(builder):
    return AnimationEnd(builder)

try:
    from typing import Optional
except:
    pass

class AnimationT(object):

    # AnimationT
    def __init__(self):
        self.info = None  # type: Optional[InfoT]
        self.skeleton = None  # type: Optional[BoneAnimationT]
        self.material = None  # type: Optional[MaterialAnimationT]
        self.visibility = None  # type: Optional[SkinAnimationT]
        self.eventData = None  # type: Optional[CommandAnimationT]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        animation = Animation()
        animation.Init(buf, pos)
        return cls.InitFromObj(animation)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, animation):
        x = AnimationT()
        x._UnPack(animation)
        return x

    # AnimationT
    def _UnPack(self, animation):
        if animation is None:
            return
        if animation.Info() is not None:
            self.info = InfoT.InitFromObj(animation.Info())
        if animation.Skeleton() is not None:
            self.skeleton = BoneAnimationT.InitFromObj(animation.Skeleton())
        if animation.Material() is not None:
            self.material = MaterialAnimationT.InitFromObj(animation.Material())
        if animation.Visibility() is not None:
            self.visibility = SkinAnimationT.InitFromObj(animation.Visibility())
        if animation.EventData() is not None:
            self.eventData = CommandAnimationT.InitFromObj(animation.EventData())

    # AnimationT
    def Pack(self, builder):
        if self.info is not None:
            info = self.info.Pack(builder)
        if self.skeleton is not None:
            skeleton = self.skeleton.Pack(builder)
        if self.material is not None:
            material = self.material.Pack(builder)
        if self.visibility is not None:
            visibility = self.visibility.Pack(builder)
        if self.eventData is not None:
            eventData = self.eventData.Pack(builder)
        AnimationStart(builder)
        if self.info is not None:
            AnimationAddInfo(builder, info)
        if self.skeleton is not None:
            AnimationAddSkeleton(builder, skeleton)
        if self.material is not None:
            AnimationAddMaterial(builder, material)
        if self.visibility is not None:
            AnimationAddVisibility(builder, visibility)
        if self.eventData is not None:
            AnimationAddEventData(builder, eventData)
        animation = AnimationEnd(builder)
        return animation
