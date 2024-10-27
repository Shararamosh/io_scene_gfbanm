# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class DynamicBooleanTrack(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DynamicBooleanTrack()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsDynamicBooleanTrack(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # DynamicBooleanTrack
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DynamicBooleanTrack
    def Bool(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.BoolFlags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # DynamicBooleanTrack
    def BoolAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.BoolFlags, o)
        return 0

    # DynamicBooleanTrack
    def BoolLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # DynamicBooleanTrack
    def BoolIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

def DynamicBooleanTrackStart(builder):
    builder.StartObject(1)

def Start(builder):
    DynamicBooleanTrackStart(builder)

def DynamicBooleanTrackAddBool(builder, bool):
    builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(bool), 0)

def AddBool(builder, bool):
    DynamicBooleanTrackAddBool(builder, bool)

def DynamicBooleanTrackStartBoolVector(builder, numElems):
    return builder.StartVector(1, numElems, 1)

def StartBoolVector(builder, numElems):
    return DynamicBooleanTrackStartBoolVector(builder, numElems)

def DynamicBooleanTrackEnd(builder):
    return builder.EndObject()

def End(builder):
    return DynamicBooleanTrackEnd(builder)

try:
    from typing import List
except:
    pass

class DynamicBooleanTrackT(object):

    # DynamicBooleanTrackT
    def __init__(self):
        self.bool = None  # type: List[bool]

    @classmethod
    def InitFromBuf(cls, buf, pos):
        dynamicBooleanTrack = DynamicBooleanTrack()
        dynamicBooleanTrack.Init(buf, pos)
        return cls.InitFromObj(dynamicBooleanTrack)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, dynamicBooleanTrack):
        x = DynamicBooleanTrackT()
        x._UnPack(dynamicBooleanTrack)
        return x

    # DynamicBooleanTrackT
    def _UnPack(self, dynamicBooleanTrack):
        if dynamicBooleanTrack is None:
            return
        if not dynamicBooleanTrack.BoolIsNone():
            if np is None:
                self.bool = []
                for i in range(dynamicBooleanTrack.BoolLength()):
                    self.bool.append(dynamicBooleanTrack.Bool(i))
            else:
                self.bool = dynamicBooleanTrack.BoolAsNumpy()

    # DynamicBooleanTrackT
    def Pack(self, builder):
        if self.bool is not None:
            if np is not None and type(self.bool) is np.ndarray:
                bool = builder.CreateNumpyVector(self.bool)
            else:
                DynamicBooleanTrackStartBoolVector(builder, len(self.bool))
                for i in reversed(range(len(self.bool))):
                    builder.PrependBool(self.bool[i])
                bool = builder.EndVector()
        DynamicBooleanTrackStart(builder)
        if self.bool is not None:
            DynamicBooleanTrackAddBool(builder, bool)
        dynamicBooleanTrack = DynamicBooleanTrackEnd(builder)
        return dynamicBooleanTrack
