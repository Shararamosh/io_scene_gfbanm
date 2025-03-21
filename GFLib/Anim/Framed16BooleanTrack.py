# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Framed16BooleanTrack(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Framed16BooleanTrack()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFramed16BooleanTrack(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Framed16BooleanTrack
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Framed16BooleanTrack
    def Frames(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 2))
        return 0

    # Framed16BooleanTrack
    def FramesAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint16Flags, o)
        return 0

    # Framed16BooleanTrack
    def FramesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed16BooleanTrack
    def FramesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

    # Framed16BooleanTrack
    def Bool(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.BoolFlags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Framed16BooleanTrack
    def BoolAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.BoolFlags, o)
        return 0

    # Framed16BooleanTrack
    def BoolLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Framed16BooleanTrack
    def BoolIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def Framed16BooleanTrackStart(builder):
    builder.StartObject(2)

def Start(builder):
    Framed16BooleanTrackStart(builder)

def Framed16BooleanTrackAddFrames(builder, frames):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(frames), 0)

def AddFrames(builder, frames):
    Framed16BooleanTrackAddFrames(builder, frames)

def Framed16BooleanTrackStartFramesVector(builder, numElems):
    return builder.StartVector(2, numElems, 2)

def StartFramesVector(builder, numElems):
    return Framed16BooleanTrackStartFramesVector(builder, numElems)

def Framed16BooleanTrackAddBool(builder, bool):
    builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(bool), 0)

def AddBool(builder, bool):
    Framed16BooleanTrackAddBool(builder, bool)

def Framed16BooleanTrackStartBoolVector(builder, numElems):
    return builder.StartVector(1, numElems, 1)

def StartBoolVector(builder, numElems):
    return Framed16BooleanTrackStartBoolVector(builder, numElems)

def Framed16BooleanTrackEnd(builder):
    return builder.EndObject()

def End(builder):
    return Framed16BooleanTrackEnd(builder)

try:
    from typing import List
except:
    pass

class Framed16BooleanTrackT(object):

    # Framed16BooleanTrackT
    def __init__(self):
        self.frames = None  # type: List[int]
        self.bool = None  # type: List[bool]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        framed16BooleanTrack = Framed16BooleanTrack()
        framed16BooleanTrack.Init(buf, pos)
        return cls.InitFromObj(framed16BooleanTrack)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, framed16BooleanTrack):
        x = Framed16BooleanTrackT()
        x._UnPack(framed16BooleanTrack)
        return x

    # Framed16BooleanTrackT
    def _UnPack(self, framed16BooleanTrack):
        if framed16BooleanTrack is None:
            return
        if not framed16BooleanTrack.FramesIsNone():
            if np is None:
                self.frames = []
                for i in range(framed16BooleanTrack.FramesLength()):
                    self.frames.append(framed16BooleanTrack.Frames(i))
            else:
                self.frames = framed16BooleanTrack.FramesAsNumpy()
        if not framed16BooleanTrack.BoolIsNone():
            if np is None:
                self.bool = []
                for i in range(framed16BooleanTrack.BoolLength()):
                    self.bool.append(framed16BooleanTrack.Bool(i))
            else:
                self.bool = framed16BooleanTrack.BoolAsNumpy()

    # Framed16BooleanTrackT
    def Pack(self, builder):
        if self.frames is not None:
            if np is not None and type(self.frames) is np.ndarray:
                frames = builder.CreateNumpyVector(self.frames)
            else:
                Framed16BooleanTrackStartFramesVector(builder, len(self.frames))
                for i in reversed(range(len(self.frames))):
                    builder.PrependUint16(self.frames[i])
                frames = builder.EndVector()
        if self.bool is not None:
            if np is not None and type(self.bool) is np.ndarray:
                bool = builder.CreateNumpyVector(self.bool)
            else:
                Framed16BooleanTrackStartBoolVector(builder, len(self.bool))
                for i in reversed(range(len(self.bool))):
                    builder.PrependBool(self.bool[i])
                bool = builder.EndVector()
        Framed16BooleanTrackStart(builder)
        if self.frames is not None:
            Framed16BooleanTrackAddFrames(builder, frames)
        if self.bool is not None:
            Framed16BooleanTrackAddBool(builder, bool)
        framed16BooleanTrack = Framed16BooleanTrackEnd(builder)
        return framed16BooleanTrack
