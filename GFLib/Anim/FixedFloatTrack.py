# automatically generated by the FlatBuffers compiler, do not modify

# namespace: Anim

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class FixedFloatTrack(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FixedFloatTrack()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFixedFloatTrack(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # FixedFloatTrack
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # FixedFloatTrack
    def Float(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def FixedFloatTrackStart(builder):
    builder.StartObject(1)

def Start(builder):
    FixedFloatTrackStart(builder)

def FixedFloatTrackAddFloat(builder, float):
    builder.PrependFloat32Slot(0, float, 0.0)

def AddFloat(builder, float):
    FixedFloatTrackAddFloat(builder, float)

def FixedFloatTrackEnd(builder):
    return builder.EndObject()

def End(builder):
    return FixedFloatTrackEnd(builder)


class FixedFloatTrackT(object):

    # FixedFloatTrackT
    def __init__(self):
        self.float = 0.0  # type: float

    @classmethod
    def InitFromBuf(cls, buf, pos):
        fixedFloatTrack = FixedFloatTrack()
        fixedFloatTrack.Init(buf, pos)
        return cls.InitFromObj(fixedFloatTrack)

    @classmethod
    def InitFromPackedBuf(cls, buf, pos=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, pos)
        return cls.InitFromBuf(buf, pos+n)

    @classmethod
    def InitFromObj(cls, fixedFloatTrack):
        x = FixedFloatTrackT()
        x._UnPack(fixedFloatTrack)
        return x

    # FixedFloatTrackT
    def _UnPack(self, fixedFloatTrack):
        if fixedFloatTrack is None:
            return
        self.float = fixedFloatTrack.Float()

    # FixedFloatTrackT
    def Pack(self, builder):
        FixedFloatTrackStart(builder)
        FixedFloatTrackAddFloat(builder, self.float)
        fixedFloatTrack = FixedFloatTrackEnd(builder)
        return fixedFloatTrack
