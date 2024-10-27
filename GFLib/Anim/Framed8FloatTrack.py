# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Framed8FloatTrack(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Framed8FloatTrack()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFramed8FloatTrack(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Framed8FloatTrack
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Framed8FloatTrack
    def Frames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Framed8FloatTrack
    def FramesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Framed8FloatTrack
    def FramesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed8FloatTrack
    def FramesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # Framed8FloatTrack
    def Float(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Float32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Framed8FloatTrack
    def FloatAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Float32Flags, o)
        return 0

    # Framed8FloatTrack
    def FloatLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed8FloatTrack
    def FloatIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def Framed8FloatTrackStart(builder):
    builder.StartObject(2)

def Start(builder):
    Framed8FloatTrackStart(builder)

def Framed8FloatTrackAddFrames(builder, frames):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(frames), 0)

def AddFrames(builder, frames):
    Framed8FloatTrackAddFrames(builder, frames)

def Framed8FloatTrackStartFramesVector(builder, numElems):
    return builder.StartVector(1, numElems, 1)

def StartFramesVector(builder, numElems):
    return Framed8FloatTrackStartFramesVector(builder, numElems)

def Framed8FloatTrackAddFloat(builder, float):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(float), 0)

def AddFloat(builder, float):
    Framed8FloatTrackAddFloat(builder, float)

def Framed8FloatTrackStartFloatVector(builder, numElems):
    return builder.StartVector(4, numElems, 4)

def StartFloatVector(builder, numElems):
    return Framed8FloatTrackStartFloatVector(builder, numElems)

def Framed8FloatTrackEnd(builder):
    return builder.EndObject()

def End(builder):
    return Framed8FloatTrackEnd(builder)

try:
    from typing import List
except:
    pass

class Framed8FloatTrackT(object):

    # Framed8FloatTrackT
    def __init__(self):
        self.frames = None  # type: List[int]
        self.float = None  # type: List[float]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        framed8FloatTrack = Framed8FloatTrack()
        framed8FloatTrack.Init(buf, pos)
        return cls.InitFromObj(framed8FloatTrack)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, framed8FloatTrack):
        x = Framed8FloatTrackT()
        x._UnPack(framed8FloatTrack)
        return x

    # Framed8FloatTrackT
    def _UnPack(self, framed8FloatTrack):
        if framed8FloatTrack is None:
            return
        if not framed8FloatTrack.FramesIsNone():
            if np is None:
                self.frames = []
                for i in range(framed8FloatTrack.FramesLength()):
                    self.frames.append(framed8FloatTrack.Frames(i))
            else:
                self.frames = framed8FloatTrack.FramesAsNumpy()
        if not framed8FloatTrack.FloatIsNone():
            if np is None:
                self.float = []
                for i in range(framed8FloatTrack.FloatLength()):
                    self.float.append(framed8FloatTrack.Float(i))
            else:
                self.float = framed8FloatTrack.FloatAsNumpy()

    # Framed8FloatTrackT
    def Pack(self, builder):
        if self.frames is not None:
            if np is not None and type(self.frames) is np.ndarray:
                frames = builder.CreateNumpyVector(self.frames)
            else:
                Framed8FloatTrackStartFramesVector(builder, len(self.frames))
                for i in reversed(range(len(self.frames))):
                    builder.PrependUint8(self.frames[i])
                frames = builder.EndVector()
        if self.float is not None:
            if np is not None and type(self.float) is np.ndarray:
                float = builder.CreateNumpyVector(self.float)
            else:
                Framed8FloatTrackStartFloatVector(builder, len(self.float))
                for i in reversed(range(len(self.float))):
                    builder.PrependFloat32(self.float[i])
                float = builder.EndVector()
        Framed8FloatTrackStart(builder)
        if self.frames is not None:
            Framed8FloatTrackAddFrames(builder, frames)
        if self.float is not None:
            Framed8FloatTrackAddFloat(builder, float)
        framed8FloatTrack = Framed8FloatTrackEnd(builder)
        return framed8FloatTrack
