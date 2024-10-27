# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy

from GFLib.Anim.sVec3 import sVec3T, sVec3

np = import_numpy()

class Framed8RotationTrack(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Framed8RotationTrack()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFramed8RotationTrack(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Framed8RotationTrack
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Framed8RotationTrack
    def Frames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Framed8RotationTrack
    def FramesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Framed8RotationTrack
    def FramesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed8RotationTrack
    def FramesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # Framed8RotationTrack
    def Co(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 6
            obj = sVec3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Framed8RotationTrack
    def CoLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed8RotationTrack
    def CoIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def Framed8RotationTrackStart(builder):
    builder.StartObject(2)

def Start(builder):
    Framed8RotationTrackStart(builder)

def Framed8RotationTrackAddFrames(builder, frames):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(frames), 0)

def AddFrames(builder, frames):
    Framed8RotationTrackAddFrames(builder, frames)

def Framed8RotationTrackStartFramesVector(builder, numElems):
    return builder.StartVector(1, numElems, 1)

def StartFramesVector(builder, numElems):
    return Framed8RotationTrackStartFramesVector(builder, numElems)

def Framed8RotationTrackAddCo(builder, co):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(co), 0)

def AddCo(builder, co):
    Framed8RotationTrackAddCo(builder, co)

def Framed8RotationTrackStartCoVector(builder, numElems):
    return builder.StartVector(6, numElems, 2)

def StartCoVector(builder, numElems):
    return Framed8RotationTrackStartCoVector(builder, numElems)

def Framed8RotationTrackEnd(builder):
    return builder.EndObject()

def End(builder):
    return Framed8RotationTrackEnd(builder)

try:
    from typing import List
except:
    pass

class Framed8RotationTrackT(object):

    # Framed8RotationTrackT
    def __init__(self):
        self.frames = None  # type: List[int]
        self.co = None  # type: List[sVec3T]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        framed8RotationTrack = Framed8RotationTrack()
        framed8RotationTrack.Init(buf, pos)
        return cls.InitFromObj(framed8RotationTrack)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, framed8RotationTrack):
        x = Framed8RotationTrackT()
        x._UnPack(framed8RotationTrack)
        return x

    # Framed8RotationTrackT
    def _UnPack(self, framed8RotationTrack):
        if framed8RotationTrack is None:
            return
        if not framed8RotationTrack.FramesIsNone():
            if np is None:
                self.frames = []
                for i in range(framed8RotationTrack.FramesLength()):
                    self.frames.append(framed8RotationTrack.Frames(i))
            else:
                self.frames = framed8RotationTrack.FramesAsNumpy()
        if not framed8RotationTrack.CoIsNone():
            self.co = []
            for i in range(framed8RotationTrack.CoLength()):
                if framed8RotationTrack.Co(i) is None:
                    self.co.append(None)
                else:
                    sVec3_ = sVec3T.InitFromObj(framed8RotationTrack.Co(i))
                    self.co.append(sVec3_)

    # Framed8RotationTrackT
    def Pack(self, builder):
        if self.frames is not None:
            if np is not None and type(self.frames) is np.ndarray:
                frames = builder.CreateNumpyVector(self.frames)
            else:
                Framed8RotationTrackStartFramesVector(builder, len(self.frames))
                for i in reversed(range(len(self.frames))):
                    builder.PrependUint8(self.frames[i])
                frames = builder.EndVector()
        if self.co is not None:
            Framed8RotationTrackStartCoVector(builder, len(self.co))
            for i in reversed(range(len(self.co))):
                self.co[i].Pack(builder)
            co = builder.EndVector()
        Framed8RotationTrackStart(builder)
        if self.frames is not None:
            Framed8RotationTrackAddFrames(builder, frames)
        if self.co is not None:
            Framed8RotationTrackAddCo(builder, co)
        framed8RotationTrack = Framed8RotationTrackEnd(builder)
        return framed8RotationTrack
