# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy

from GFLib.Anim.Vec3 import Vec3, Vec3T

np = import_numpy()

class Framed8VectorTrack(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Framed8VectorTrack()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFramed8VectorTrack(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Framed8VectorTrack
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Framed8VectorTrack
    def Frames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Framed8VectorTrack
    def FramesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Framed8VectorTrack
    def FramesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed8VectorTrack
    def FramesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # Framed8VectorTrack
    def Co(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 12
            obj = Vec3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Framed8VectorTrack
    def CoLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed8VectorTrack
    def CoIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def Framed8VectorTrackStart(builder):
    builder.StartObject(2)

def Start(builder):
    Framed8VectorTrackStart(builder)

def Framed8VectorTrackAddFrames(builder, frames):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(frames), 0)

def AddFrames(builder, frames):
    Framed8VectorTrackAddFrames(builder, frames)

def Framed8VectorTrackStartFramesVector(builder, numElems):
    return builder.StartVector(1, numElems, 1)

def StartFramesVector(builder, numElems):
    return Framed8VectorTrackStartFramesVector(builder, numElems)

def Framed8VectorTrackAddCo(builder, co):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(co), 0)

def AddCo(builder, co):
    Framed8VectorTrackAddCo(builder, co)

def Framed8VectorTrackStartCoVector(builder, numElems):
    return builder.StartVector(12, numElems, 4)

def StartCoVector(builder, numElems):
    return Framed8VectorTrackStartCoVector(builder, numElems)

def Framed8VectorTrackEnd(builder):
    return builder.EndObject()

def End(builder):
    return Framed8VectorTrackEnd(builder)

try:
    from typing import List
except:
    pass

class Framed8VectorTrackT(object):

    # Framed8VectorTrackT
    def __init__(self):
        self.frames = None  # type: List[int]
        self.co = None  # type: List[Vec3T]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        framed8VectorTrack = Framed8VectorTrack()
        framed8VectorTrack.Init(buf, pos)
        return cls.InitFromObj(framed8VectorTrack)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, framed8VectorTrack):
        x = Framed8VectorTrackT()
        x._UnPack(framed8VectorTrack)
        return x

    # Framed8VectorTrackT
    def _UnPack(self, framed8VectorTrack):
        if framed8VectorTrack is None:
            return
        if not framed8VectorTrack.FramesIsNone():
            if np is None:
                self.frames = []
                for i in range(framed8VectorTrack.FramesLength()):
                    self.frames.append(framed8VectorTrack.Frames(i))
            else:
                self.frames = framed8VectorTrack.FramesAsNumpy()
        if not framed8VectorTrack.CoIsNone():
            self.co = []
            for i in range(framed8VectorTrack.CoLength()):
                if framed8VectorTrack.Co(i) is None:
                    self.co.append(None)
                else:
                    vec3_ = Vec3T.InitFromObj(framed8VectorTrack.Co(i))
                    self.co.append(vec3_)

    # Framed8VectorTrackT
    def Pack(self, builder):
        if self.frames is not None:
            if np is not None and type(self.frames) is np.ndarray:
                frames = builder.CreateNumpyVector(self.frames)
            else:
                Framed8VectorTrackStartFramesVector(builder, len(self.frames))
                for i in reversed(range(len(self.frames))):
                    builder.PrependUint8(self.frames[i])
                frames = builder.EndVector()
        if self.co is not None:
            Framed8VectorTrackStartCoVector(builder, len(self.co))
            for i in reversed(range(len(self.co))):
                self.co[i].Pack(builder)
            co = builder.EndVector()
        Framed8VectorTrackStart(builder)
        if self.frames is not None:
            Framed8VectorTrackAddFrames(builder, frames)
        if self.co is not None:
            Framed8VectorTrackAddCo(builder, co)
        framed8VectorTrack = Framed8VectorTrackEnd(builder)
        return framed8VectorTrack
